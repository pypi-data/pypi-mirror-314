import copy
import logging
import warnings
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Generator, Hashable, MutableMapping

from sentineltoolbox._utils import _get_attr_dict, string_to_slice
from sentineltoolbox.hotfix import (
    Hotfix,
    HotfixManager,
    HotfixPath,
    HotfixValue,
    load_hotfix,
)
from sentineltoolbox.models.filename_generator import extract_semantic
from sentineltoolbox.resources.data import (
    DATAFILE_METADATA,
    ProductMetadataResource,
    ResourceDb,
)
from sentineltoolbox.typedefs import (
    MetadataType_L,
    T_Attributes,
    T_ContainerWithAttributes,
    category_paths,
)
from sentineltoolbox.writers.json import serialize_to_zarr_json

logger = logging.getLogger("sentineltoolbox")

__all__ = ["AttributeHandler"]


def guess_product_type(obj: T_ContainerWithAttributes | T_Attributes, **kwargs: Any) -> str:
    ptype = kwargs.get("product_type", "")
    if not ptype:
        attrs = _get_attr_dict(obj)
        try:
            info = obj.reader_info  # type: ignore
        except AttributeError:
            ptype = attrs.get("stac_discovery", {}).get("properties", {}).get("product:type", "")
        else:
            semantic = extract_semantic(info.get("name", ""))
            ptype = DATAFILE_METADATA.get_metadata(semantic, "product:type", "")
            if not ptype:
                ptype = attrs.get("stac_discovery", {}).get("properties", {}).get("product:type", "")
    return ptype


def recursive_update(
    d1: Dict[Hashable, Any],
    d2: Dict[Hashable, Any],
    mode_for_dict: str = "merge",
    mode_for_list: str = "replace",
    mode_for_set: str = "replace",
) -> None:
    """
    Recursively updates dictionary `d1` with values from `d2`,
    allowing separate modes for handling dictionaries, lists, and sets.

    Arguments:
    - d1: The destination dictionary to update.
    - d2: The source dictionary to update from.
    - mode_for_dict: The update mode for dictionaries (default: "replace"):
        - "replace": Overwrite existing keys.
        - "add": Add only new keys.
        - "merge": Recursively merge keys.
    - mode_for_list: The update mode for lists (default: "replace"):
        - "replace": Overwrite existing lists.
        - "merge": Concatenate lists.
    - mode_for_set: The update mode for sets (default: "replace"):
        - "replace": Overwrite existing sets.
        - "merge": Union of sets.

    Returns:
    - The updated dictionary `d1`.
    """
    for key, value in d2.items():
        if key in d1:
            if isinstance(value, dict) and isinstance(d1[key], dict):
                if mode_for_dict == "merge":
                    recursive_update(
                        d1[key],
                        copy.copy(value),
                        mode_for_dict=mode_for_dict,
                        mode_for_list=mode_for_list,
                        mode_for_set=mode_for_set,
                    )
                elif mode_for_dict == "replace":
                    d1[key] = value
                elif mode_for_dict == "add":
                    pass  # Keep existing keys, do nothing
            elif isinstance(value, list) and isinstance(d1[key], list):
                if mode_for_list == "merge":
                    d1[key].extend(value)
                elif mode_for_list == "replace":
                    d1[key] = copy.copy(value)
            elif isinstance(value, set) and isinstance(d1[key], set):
                if mode_for_set == "merge":
                    d1[key].update(value)
                elif mode_for_set == "replace":
                    d1[key] = copy.copy(value)
            else:
                if isinstance(d1[key], (list, dict, set)):
                    # We try to update a dict, set or list with something not compatible, keep initial value
                    logger.warning(f"Cannot update data of type {type(d1[key])} with data of type {type(value)}")
                else:
                    d1[key] = value  # For non-iterable types, always replace
        else:
            d1[key] = copy.deepcopy(value)  # Add new keys from d2


def path_relative_to_category(path: str, category: MetadataType_L | None, **kwarg: Any) -> str:
    if category in ("stac_properties", "stac_discovery", "metadata"):
        return path.replace(category_paths[category], "")
    else:
        return path


def fix_attribute_value(path: str, value: Any, category: MetadataType_L | None, **kwargs: Any) -> Any:

    for hotfix in get_hotfix_manager(**kwargs).value():
        new_value = value
        relpath = path_relative_to_category(path, category, **kwargs)

        conversions = hotfix.data.get(category, {})
        if relpath in conversions:
            fix_function = conversions[relpath]
            new_value = fix_function(value, path=path, **kwargs)

        return new_value
    return value


def to_json(path: str, value: Any, category: MetadataType_L | None, **kwargs: Any) -> Any:
    relpath = path_relative_to_category(path, category, **kwargs)
    for hotfix in get_hotfix_manager(**kwargs).wrapper():
        conversions = hotfix.data.get(category, {})
        if relpath in conversions:
            converter = conversions[relpath]
            return converter.to_json(value, path=path)

    return value


def from_json(path: str, value: Any, category: MetadataType_L | None, **kwargs: Any) -> Any:
    relpath = path_relative_to_category(path, category, **kwargs)

    for hotfix in get_hotfix_manager(**kwargs).wrapper():
        conversions = hotfix.data.get(category, {})
        if relpath in conversions:
            converter = conversions[relpath]
            return converter.from_json(value, path=path)

    return value


def guess_category(path: str, **kwargs: Any) -> MetadataType_L | None:
    category = kwargs.get("category")
    if category is not None:
        return category
    if path.startswith("properties") or path.startswith("stac_discovery/properties"):
        return "stac_properties"
    elif path.startswith("stac_discovery"):
        return "stac_discovery"
    elif path.startswith("other_metadata") or path.startswith("metadata"):
        return "metadata"
    else:
        return get_hotfix_manager(**kwargs).get_alias(path)[0]


def fix_attribute_path(
    path: str,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> tuple[str, MetadataType_L | None]:
    """
    Adjusts the given attribute path to match a canonical format based on its category.
    Applies hotfixes if specified. Look at short names (alias_dict)

    >>> fix_attribute_path("properties/test", category="stac_properties")
    ('stac_discovery/properties/test', 'stac_properties')
    >>> fix_attribute_path("test", category="stac_properties")
    ('stac_discovery/properties/test', 'stac_properties')
    >>> fix_attribute_path("properties/test") # category is recognized here
    ('stac_discovery/properties/test', 'stac_properties')
    >>> fix_attribute_path("properties/test", category="metadata") # category is recognized but fix trust user inputs
    ('other_metadata/test', 'metadata')
    >>> fix_attribute_path("test") # category not recognized, no user inputs => path unchanged
    ('test', None)

    Use short names if provided
    >>> fix_attribute_path("eo:bands", alias_dict={"eo:bands":("stac_properties", "bands")})
    ('stac_discovery/properties/bands', 'stac_properties')

    Args:
        path: The initial attribute path.
        category: The category of the attribute (e.g., "stac_properties", "metadata").
        **kwargs: Additional options, including a "hotfix_list" for path adjustments.

    Returns:
        The corrected and fixed attribute path.
    """
    # Clean up the provided path
    path = path.strip().rstrip("/")

    # Resolve the category and path using aliases, if applicable
    if category is None:
        category, path = get_hotfix_manager(**kwargs).get_alias(path)

    # Attempt to determine the category if not already provided
    if category is None:
        category = guess_category(path, **kwargs)

    if category is None:
        # If the category cannot be determined, return the path unchanged
        return path, None

    # Determine the appropriate prefix based on the category
    if category == "stac_properties":
        prefix = "stac_discovery/properties/"
    elif category == "stac_discovery":
        prefix = "stac_discovery/"
    elif category == "metadata":
        prefix = "other_metadata/"
    else:
        prefix = ""

    # Strip any existing recognized prefixes from the path

    # Define recognized prefixes for different categories
    recognized_properties = ["stac_discovery/properties/", "properties/"]
    recognized_stac = ["stac_discovery/"]
    recognized_metadata = ["other_metadata/", "metadata/"]
    recognized_prefixes = recognized_properties + recognized_stac + recognized_metadata

    for possible_prefix in recognized_prefixes:
        prefix_parts = possible_prefix.split("/")

        for prefix_part in prefix_parts:
            if prefix_part and path.startswith(prefix_part):
                # Remove the matched prefix from the path
                path = path[len(prefix_part) + 1 :]  # noqa: E203 (whitespace issue in slicing)

    final_path = prefix + path
    for hotfix in get_hotfix_manager(**kwargs).path():
        try:
            category, final_path = hotfix.data[final_path]
        except KeyError:
            pass
        else:
            # volountary force hotfix list to empty to avoid recursion error, for example
            # if user write fix like "stac_discovery/properties/eo:bands" -> ("stac_properties", "eo:bands")
            return fix_attribute_path(final_path, category, hotfix=HotfixManager([]))

    # Prepend the determined prefix to the stripped path
    return final_path, category


def _get_value_from_path(group: T_Attributes, path: str, **kwargs: Any) -> Any:
    """
    Extract value at path. No path fix. If path is wrong => KeyError
    """
    path = path.strip().rstrip("/")
    # Determine if value conversion should be performed
    convert_value_type = kwargs.get("convert_value_type", True)
    real_path_parts = []

    parts: list[str] = path.split("/")  # Split the path into components
    value_found = False
    msg = path

    # Traverse the path parts within the current location
    for part in parts:
        try:
            # Attempt to convert the part to an integer for list indexing
            valid_part: int | slice | str = int(part)
        except ValueError:
            try:
                # Attempt to interpret the part as a slice
                valid_part = string_to_slice(part)
            except ValueError:
                valid_part = part  # Default to a string if conversion fails

        if isinstance(valid_part, (int, slice)):
            # Handle list indexing
            real_path_parts.append(part)
            if isinstance(group, list):
                group = group[valid_part]
                value_found = True
            else:
                raise KeyError(
                    f"Invalid path {path!r}. Part {valid_part!r} is not correct because {group} is not a list",
                )
        else:
            # Handle dictionary key access
            _kwargs = copy.copy(kwargs)
            _kwargs["warn_deprecated"] = False
            if part in group:
                value_found = True
                group = group[part]
                real_path_parts.append(part)
            else:
                # Stop further processing if the key is not found
                value_found = False
                if part != parts[0]:
                    valid_part = "/".join(real_path_parts)
                    msg = f"{path}. {valid_part} exists but not {part}"
                break

    if value_found:
        if convert_value_type:
            category = guess_category(path, **kwargs)
            value = fix_attribute_value(path, group, category=category, **kwargs)
        else:
            value = group
        return value
    else:
        raise KeyError(msg)


def find_and_fix_attribute(
    attrs: T_Attributes,  # The attributes dictionary or object to search in
    path: str,  # The path to the attribute to locate
    *,
    category: MetadataType_L | None = None,  # The category of the attribute (optional)
    **kwargs: Any,  # Additional options, such as conversion settings or defaults
) -> tuple[Any, str, str]:  # Returns the found value, fixed path, and real path
    """
    Finds an attribute in a hierarchical structure and optionally fixes its path or value.
    Creates a new attribute if requested and not found.

    Args:
        attrs: The attributes dictionary or object to search within.
        fixed_path: The path of the attribute to find.
        category: The category of the attribute, if known.
        **kwargs: Additional options like 'convert_value_type', 'default', or 'create'.

    Returns:
        A tuple of the found value, the fixed path, and the real path.

    Raises:
        KeyError: If the attribute is not found and no default is specified.
    """

    # convert input path to canonical path
    user_path = path
    fixed_path, category = fix_attribute_path(path, category, **kwargs)

    # Now that path is correct, tries to return it
    err_msg = ""
    try:
        return _get_value_from_path(attrs, fixed_path, **kwargs), fixed_path, fixed_path
    except KeyError as err:
        err_msg = err.args[0]

    # If not found tries to search with user path not fixed
    try:
        return _get_value_from_path(attrs, user_path, **kwargs), fixed_path, user_path
    except KeyError as err:
        err_msg = err.args[0]

    # If not found, search in probable places
    # Define potential search locations based on the category
    places_properties = [
        ("stac_discovery/properties/", attrs.get("stac_discovery", {}).get("properties")),
        ("properties/", attrs.get("properties")),
    ]
    places_metadata = [
        ("other_metadata/", attrs.get("other_metadata")),
        ("metadata/", attrs.get("metadata")),
    ]
    places_stac = [
        ("stac_discovery/", attrs.get("stac_discovery")),
    ]
    places_root: list[tuple[str, Any]] = [("", attrs)]

    # Select search places based on category
    if category == "stac_properties":
        # Search order: stac_discovery/properties -> properties -> root
        places = places_properties + places_root
    elif category == "metadata":
        # Search order: other_metadata -> metadata -> root
        places = places_metadata + places_root
    elif category == "stac_discovery":
        # Search order: stac_discovery -> root
        places = places_stac + places_root
    elif category == "root":
        # Only root-level attributes
        places = places_root
    else:
        # Default to searching all places if the category is unknown
        category = None
        places = places_root + places_properties + places_stac + places_metadata

    # Iterate over the possible locations to find the attribute
    for place_path, place in places:
        if place is None:
            continue  # Skip if the current location is invalid

        paths: list[str] = []
        fixed_path, category = fix_attribute_path(fixed_path, category, **kwargs)
        paths.append(fixed_path)
        path = path_relative_to_category(fixed_path, category, **kwargs)
        paths.append(path)

        paths.append(user_path)
        path = path_relative_to_category(user_path, category, **kwargs)
        paths.append(path)

        for path in paths:
            try:
                value = _get_value_from_path(place, path, **kwargs)
            except KeyError:
                pass
            else:
                return value, fixed_path, place_path + path

    # Handle the case where the attribute is not found
    if "default" in kwargs or "create" in kwargs:
        default = kwargs.get("default")
        if "create" in kwargs:
            set_attr(attrs, fixed_path, default, category=category, **kwargs)
            return default, fixed_path, fixed_path
        else:
            return default, fixed_path, ""
    else:
        raise KeyError(err_msg)


def recurse_json_dict(
    d: MutableMapping[Any, Any] | list[Any],
    root: str = "",
) -> Generator[tuple[str, Any], None, None]:
    if isinstance(d, dict):
        items = list(d.items())
    elif isinstance(d, list):
        items = [(str(i), v) for i, v in enumerate(d)]
    else:
        items = []

    for k, v in items:
        path = root + k + "/"
        yield path, v
        if isinstance(v, (dict, list)):
            yield from recurse_json_dict(v, path)


def search_attributes(
    attrs: T_ContainerWithAttributes | T_Attributes,
    path: str,
    *,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> list[str]:
    kwargs["warn_deprecated"] = kwargs.get("warn_deprecated", False)
    kwargs["convert_value_type"] = kwargs.get("convert_value_type", False)
    recursive = kwargs.get("recursive", True)
    limit = kwargs.get("limit")

    dict_attrs: T_Attributes = _get_attr_dict(attrs)
    results = set()

    try:
        value, fixed, real = find_and_fix_attribute(dict_attrs, path, category=category, **kwargs)
        results.add(real)
    except KeyError:
        pass

    if recursive:
        for p, v in recurse_json_dict(dict_attrs):
            if isinstance(limit, int) and len(results) > limit:
                break
            if not isinstance(v, dict):
                continue
            current_category = guess_category(p, **kwargs)
            if category is not None and current_category != category:
                continue
            try:
                value, fixed, real = find_and_fix_attribute(v, path, category=category, **kwargs)
            except KeyError:
                pass
            else:
                results.add(p + real)
    return list(sorted(results))


def extract_attr(
    data: T_ContainerWithAttributes | T_Attributes,
    path: str | None = None,
    *,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> Any:
    attrs = _get_attr_dict(data)
    if path is None:
        if category is None:
            return attrs
        else:
            category_path = category_paths[category]
            return extract_attr(attrs, category_path, **kwargs)
    else:
        value, fixed_path, real_path = find_and_fix_attribute(attrs, path, category=category, **kwargs)
        if category is None:
            category = "root"
        return from_json(fixed_path, value, category=guess_category(fixed_path, category=category, **kwargs), **kwargs)


def set_attr(
    data: T_ContainerWithAttributes | T_Attributes,
    path: str,
    value: Any,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> MutableMapping[Any, Any]:
    root_attrs = _get_attr_dict(data)
    path, category = fix_attribute_path(path, category=category, **kwargs)
    category = guess_category(path, category=category, **kwargs)
    if category is None:
        category = "root"
    attrs = root_attrs
    parts = path.split("/")
    for part in parts[:-1]:
        attrs = attrs.setdefault(part, {})
    if kwargs.get("fix", True):
        old_value = value
        value = fix_attribute_value(path, value, category=category, **kwargs)
        if value != old_value:
            logger.info(f"{path}: value {old_value!r} has been fixed to {value!r}")
    if kwargs.get("format", True):
        value = from_json(path, value, category=category, **kwargs)
    attrs[parts[-1]] = to_json(path, value, category=category, **kwargs)
    return root_attrs


def append_log(container: T_ContainerWithAttributes, log_data: Any, **kwargs: Any) -> None:
    """
    See :obj:`AttributeHandler.append_log`

    :param container: container to update
    """
    AttributeHandler(container, **kwargs).append_log(log_data, **kwargs)


def get_logs(container: T_ContainerWithAttributes, **kwargs: Any) -> list[Any]:
    """
    See :obj:`AttributeHandler.get_logs`

    :param container: container containing log metadata
    """
    return AttributeHandler(container, **kwargs).get_logs(**kwargs)


def _extract_namespace_name(attribute_handler_name: str | None, **kwargs: Any) -> tuple[str, str]:
    namespace = kwargs.get("namespace", "processing_unit_history")
    name = kwargs.get("name", attribute_handler_name if attribute_handler_name is not None else "root")
    return namespace, name


def get_hotfix_manager(**kwargs: Any) -> HotfixManager:
    hotfix_list = copy.copy(kwargs.get("hotfix_list", []))
    if "alias_dict" in kwargs:
        hotfix_list.append(
            HotfixPath(kwargs["alias_dict"], name="Alias Fix", description="Fix alias from user aliases", priority=2),
        )

    return kwargs.get("hotfix", HotfixManager(hotfix_list))


class AttributeHandler:
    """
    TODO: if set, read stac_discovery/stac_extensions to automatically recognize stac properties.
    For examlple, if view is in stac_extension, help('view:incidence_angle') automatically understand that
    "view:incidence_angle" is equivalent to "stac_discovery/properties/view:incidence_angle"
    """

    def __init__(self, container: T_ContainerWithAttributes | T_Attributes | None = None, **kwargs: Any):
        """

        :param container:
        :param kwargs:
          - template: template name to use
          - context: template context
          - name:
        """
        if container is None:
            container = {}
        self._container = container
        self.name = kwargs.get("name")
        self._kwargs = kwargs
        self._kwargs["hotfix"] = get_hotfix_manager(
            hotfix_list=kwargs.get("hotfix_list", load_hotfix()),
            alias_dict=kwargs.get("alias_dict", {}),
        )
        try:
            info = container.reader_info  # type: ignore
        except AttributeError:
            pass
        else:
            semantic = extract_semantic(info.get("name", ""))
            ptype = DATAFILE_METADATA.get_metadata(semantic, "product:type")
            if ptype:
                self.set_attr("product:type", ptype)

    def to_dict(self) -> MutableMapping[Any, Any]:
        """

        :return: convert it to dict. If container is a dict, return a copy of it
        """
        return copy.copy(_get_attr_dict(self._container))

    def container(self) -> Any:
        return self._container

    def append_log(self, log_data: Any, **kwargs: Any) -> None:
        """
        :param log_data: data you want to log
        :param kwargs:
          * name: processing unit name. Default: AttributeHandler.name or `"root"` if not set
          * namespace: group containing all logs. Default: `"processing_unit_history"`
        :return:
        """
        serialized_data = serialize_to_zarr_json(log_data, errors="replace", **kwargs)
        namespace, name = _extract_namespace_name(self.name, **kwargs)
        history = self.get_metadata(namespace, create=True, default={})
        history.setdefault(name, []).append(serialized_data)

    def get_logs(self, **kwargs: Any) -> list[Any]:
        """
        :param kwargs:
          * name: processing unit name. Default: AttributeHandler.name or `"root"` if not set
          * namespace: group containing all logs. Default: `"processing_unit_history"`
        :return: all logs registered in products
        """
        namespace, name = _extract_namespace_name(self.name, **kwargs)
        return self.get_metadata(f"{namespace}/{name}", default=[])

    def _update_kwargs(self, kwargs: Any) -> dict[str, Any]:
        final_kwargs: dict[str, Any] = {}
        final_kwargs.update(self._kwargs)
        final_kwargs.update(kwargs)
        return final_kwargs

    def set_property(self, path: str, value: Any, **kwargs: Any) -> None:
        warnings.warn("use set_stac_property instead", DeprecationWarning)
        self.set_stac_property(path, value, **kwargs)

    def set_stac_property(self, path: str, value: Any, **kwargs: Any) -> None:
        kwargs = self._update_kwargs(kwargs)
        set_attr(self._container, path, value, category="stac_properties", **kwargs)

    def set_metadata(self, path: str, value: Any, **kwargs: Any) -> None:
        kwargs = self._update_kwargs(kwargs)
        set_attr(self._container, path, value, category="metadata", **kwargs)

    def set_stac(self, path: str, value: Any, **kwargs: Any) -> None:
        kwargs = self._update_kwargs(kwargs)
        set_attr(self._container, path, value, category="stac_discovery", **kwargs)

    def set_root_attr(self, path: str, value: Any, **kwargs: Any) -> None:
        kwargs = self._update_kwargs(kwargs)
        set_attr(self._container, path, value, category="root", **kwargs)

    def set_attr(self, path: str, value: Any, category: MetadataType_L | None = None, **kwargs: Any) -> None:
        kwargs = self._update_kwargs(kwargs)
        set_attr(self._container, path, value, category=category, **kwargs)

    def get_attr(self, path: str | None = None, category: MetadataType_L | None = None, **kwargs: Any) -> Any:
        kwargs = self._update_kwargs(kwargs)
        return extract_attr(self._container, path, category=category, **kwargs)

    def get_stac_property(self, path: str | None = None, **kwargs: Any) -> Any:
        kwargs = self._update_kwargs(kwargs)
        return extract_attr(self._container, path, category="stac_properties", **kwargs)

    def get_metadata(self, path: str | None = None, **kwargs: Any) -> Any:
        kwargs = self._update_kwargs(kwargs)
        return extract_attr(self._container, path, category="metadata", **kwargs)

    def get_stac(self, path: str | None = None, **kwargs: Any) -> Any:
        kwargs = self._update_kwargs(kwargs)
        return extract_attr(self._container, path, category="stac_discovery", **kwargs)

    def get_root_attr(self, path: str | None = None, **kwargs: Any) -> Any:
        kwargs = self._update_kwargs(kwargs)
        return extract_attr(self._container, path, category="root", **kwargs)

    def search(
        self,
        path: str,
        *,
        category: MetadataType_L | None = None,
        **kwargs: Any,
    ) -> list[str]:
        kwargs = self._update_kwargs(kwargs)
        return search_attributes(self._container, path, category=category, **kwargs)

    def fix_path(self, path: str, **kwargs: Any) -> str:
        kwargs = self._update_kwargs(kwargs)
        return fix_attribute_path(path, **kwargs)[0]

    def _help(
        self,
        path: str,
        description_data: list[Any],
        documentation_data: list[Any],
        **kwargs: Any,
    ) -> dict[str, Any]:
        kwargs = self._update_kwargs(kwargs)
        help_data = {}
        attrs = _get_attr_dict(self._container)
        try:
            value, fixed, real = find_and_fix_attribute(attrs, path, **kwargs)
        except KeyError:
            pass
        else:

            help_data["value"] = value
            path = real
        category = guess_category(path, **kwargs)
        path = self.fix_path(path, category=category)
        name = Path(path).name
        if category:
            help_data["category"] = category
            help_data["path"] = path
        if category == "stac_properties":
            from sentineltoolbox.stacutils import STAC_PROPERTIES

            try:
                data, _, _ = find_and_fix_attribute(STAC_PROPERTIES, name, category=category, **kwargs)
            except KeyError:
                pass
            else:
                help_data.update(copy.copy(data))
        for field, field_dbs in [
            ("description", description_data),
            ("documentation", documentation_data),
        ]:
            for db in field_dbs:
                try:
                    found, _, _ = find_and_fix_attribute(db, name, **kwargs)
                except KeyError:
                    pass
                else:
                    if found is None:
                        continue
                    help_data[field] = found
                    break
        return help_data

    def apply_hotfix(self, hotfix: Hotfix, attrs: MutableMapping[Hashable, Any]) -> None:
        if hotfix.hotfix_type == "path":
            for wrong_path, correct_data in hotfix.data.items():
                correct_cat, correct_rel_path = correct_data
                correct_path, correct_cat = fix_attribute_path(correct_rel_path, correct_cat)
                try:
                    value = _get_value_from_path(attrs, wrong_path)
                except KeyError:
                    pass
                else:
                    if correct_path != wrong_path:
                        pp = PurePosixPath(wrong_path)
                        parent = pp.parent.as_posix()
                        if parent == ".":
                            old_data = attrs
                            del old_data[pp.name]
                        else:
                            old_data = self.get_attr(parent)
                            del old_data[pp.name]
                    self.set_attr(correct_path, value, category=correct_cat)

        elif hotfix.hotfix_type == "value":
            for category, attr_dict in hotfix.data.items():
                if category.startswith("/"):
                    try:
                        root = self._container[category]
                    except KeyError:
                        attribute_handler = self
                    else:
                        local_hotfix = HotfixValue({"root": attr_dict})
                        attribute_handler = AttributeHandler(root, hotfix_list=[local_hotfix])
                        category = "root"
                else:
                    attribute_handler = self
                for attr_relpath in attr_dict:
                    try:
                        current_value = attribute_handler.get_attr(attr_relpath, category=category)
                    except KeyError:
                        pass
                    else:
                        attribute_handler.set_attr(attr_relpath, current_value, category=category)

        elif hotfix.hotfix_type == "wrapper":
            for category, attr_dict in hotfix.data.items():
                for attr_relpath, converter in attr_dict.items():
                    try:
                        current_value = self.get_attr(attr_relpath, category=category)
                    except KeyError:
                        pass
                    else:
                        fixed_value = converter.to_json(converter.from_json(current_value))
                        self.set_attr(attr_relpath, fixed_value, category=category)

    def fix(self, **kwargs: Any) -> None:
        kwargs = self._update_kwargs(kwargs)
        hotfix_manager = get_hotfix_manager(**kwargs)
        attrs = _get_attr_dict(self._container)
        product_type = guess_product_type(self._container)
        if attrs is None:
            attrs = {}
        for hotfix in hotfix_manager.hotfix_list:
            if not hotfix.is_applicable(attrs, product_type):
                continue
            logger.info(f"apply hotfix <{hotfix.name}> {hotfix.description} (priority={hotfix.priority})")
            self.apply_hotfix(hotfix, attrs)

    def help_product(self, path: str, **kwargs: Any) -> dict[Any, Any]:
        kwargs = self._update_kwargs(kwargs)
        metadata = ProductMetadataResource(data=None, relpath="metadata/datafiles.json", **kwargs)
        description_data = [metadata.map("description")]
        documentation_data = [metadata.map("documentation")]

        return self._help(path, description_data, documentation_data, **kwargs)

    def help_attr(self, path: str, **kwargs: Any) -> dict[Any, Any]:
        kwargs = self._update_kwargs(kwargs)
        properties = ResourceDb(relpath="metadata/properties.json", **kwargs)
        terms = ResourceDb(relpath="metadata/terms.json", **kwargs)

        description_data = [properties.map("description"), terms.map("description")]
        documentation_data = [properties.map("documentation"), terms.map("documentation")]

        return self._help(path, description_data, documentation_data, **kwargs)

    def help(self, path: str, **kwargs: Any) -> dict[Any, Any]:
        kwargs = self._update_kwargs(kwargs)
        return self.help_attr(path, **kwargs)
