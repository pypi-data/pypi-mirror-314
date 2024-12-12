from typing import Any, Hashable

from datatree import DataTree

from sentineltoolbox.attributes import AttributeHandler, guess_product_type
from sentineltoolbox.hotfix import (
    ConverterDateTime,
    HotfixDataTree,
    HotfixPath,
    HotfixPathInput,
    HotfixValue,
    HotfixValueInput,
    HotfixWrapper,
    to_int,
    to_lower,
)
from sentineltoolbox.resources.data import DATAFILE_METADATA
from sentineltoolbox.typedefs import Converter, DataTreeVisitor, MetadataType_L

#################################################
# WRAPPERS
#################################################
# A wrapper simplifies the user's experience by automatically converting raw data into
# high-level Python types on the fly. For example, a date string is returned as a datetime object.
# It also performs the reverse conversion: if the user sets a datetime object, it is converted
# back to a string to support serialization.

# category / relative path -> Wrapper
WRAPPERS_GENERIC_FUNCTIONS: dict[MetadataType_L, dict[str, Converter]] = {
    "stac_properties": {
        "created": ConverterDateTime(),
        "end_datetime": ConverterDateTime(),
        "start_datetime": ConverterDateTime(),
    },
    "stac_discovery": {},
    "metadata": {},
    "root": {},
}

#################################################
# PATHS FIXES & SHORT NAMES
#################################################
# A "path fix" automatically replaces outdated or incorrect paths with valid ones.
# This is useful for all metadata where the name has changed.

# wrong path -> valid_category, valid_path
HOTFIX_PATHS_GENERIC: HotfixPathInput = {
    # {"name": ("category", None)}  if short name is equal to attribute path relative to category.
    #  This is equivalent to {"name": ("category", "name")}
    # {"short name": ("category", "relative path name")}  if short name is different
    # Ex: {"b0_id": ("stac_properties", "bands/0/name")}
    # {"/absolute/wrong/path": ("category", "relative/path")}
    # Ex: {"other_metadata/start_time": ("stac_properties", None)}
    # short names
    "bands": ("stac_properties", None),
    "created": ("stac_properties", None),
    "datatake_id": ("stac_properties", None),
    "datetime": ("stac_properties", None),
    "end_datetime": ("stac_properties", None),
    "eo:bands": ("stac_properties", "bands"),
    "eopf": ("stac_properties", None),
    "eopf:datastrip_id": ("stac_properties", None),
    "eopf:instrument_mode": ("stac_properties", None),
    "eopf:timeline": ("stac_properties", "product:timeline"),
    "eopf:type": ("stac_properties", "product:type"),
    "gsd": ("stac_properties", None),
    "instrument": ("stac_properties", None),
    "mission": ("stac_properties", None),
    "platform": ("stac_properties", None),
    "processing:level": ("stac_properties", None),
    "processing:version": ("stac_properties", None),
    "product:timeline": ("stac_properties", None),
    "product:type": ("stac_properties", None),
    "providers": ("stac_properties", None),
    "start_datetime": ("stac_properties", None),
    "updated": ("stac_properties", None),
    # wrong paths
    "stac_discovery/properties/eo:bands": ("stac_properties", "bands"),
    "stac_discovery/properties/eopf:type": ("stac_properties", "product:type"),
    "stac_discovery/properties/eopf:timeline": ("stac_properties", "product:timeline"),
}


#################################################
# VALUE FIXES
#################################################
# Function used to fix definitely value

# category / relative path -> fix functions
HOTFIX_VALUES_GENERIC: HotfixValueInput = {
    "stac_properties": {
        "platform": to_lower,
        "mission": to_lower,
        "instrument": to_lower,
        "sat:relative_orbit": to_int,
    },
    "stac_discovery": {},
    "metadata": {},
    "root": {},
}


class FixAdfMetadata(DataTreeVisitor):

    def visit_attrs(self, root: DataTree[Any], path: str, obj: dict[Hashable, Any]) -> None:
        if "long_name" in obj:
            obj["description"] = obj.pop("long_name")

        if path == "/":
            ptype = guess_product_type(root)
            metadata = DATAFILE_METADATA.get_metadata(ptype)
            if metadata:
                attrs = AttributeHandler(obj)
                for attr_name in ("product:type", "processing:level", "mission", "instrument"):
                    value = metadata.get(attr_name)
                    if value:
                        attrs.set_attr(attr_name, value)


HOTFIX = [
    HotfixValue(
        HOTFIX_VALUES_GENERIC,
        priority=1,
        name="Generic Metadata Fix",
        description="Fix platform, instrument, ...",
    ),
    HotfixPath(HOTFIX_PATHS_GENERIC, priority=1, name="Generic Path Fix", description="Fix eopf:type, ..."),
    HotfixWrapper(
        WRAPPERS_GENERIC_FUNCTIONS,
        priority=1,
        name="Generic Wrappers",
        description="wrap dates<->datetime.",
    ),
    HotfixDataTree(FixAdfMetadata(), priority=10, name="Add metadata", description="Add product:type, level, ..."),
]
