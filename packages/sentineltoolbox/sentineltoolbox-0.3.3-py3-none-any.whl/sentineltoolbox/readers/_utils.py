import copy
import json
import logging
from pathlib import Path
from typing import Any, BinaryIO, Hashable, Literal

import numpy as np
import tomli

from sentineltoolbox.typedefs import is_eopf_adf

logger = logging.getLogger("sentineltoolbox")


L_SUPPORTED_FORMATS = Literal[".json", ".toml", ".txt", None]

stb_open_parameters = (
    "secret_alias",
    "logger",
    "credentials",
    "configuration",
    "filesystem",
    "cache",
    "uncompress",
    "local_copy_dir",
    "autofix_args",
    "load",
)


def load_toml_fp(fp: BinaryIO) -> dict[str, Any]:
    with fp:
        return tomli.load(fp)


def load_toml(path: Path) -> dict[str, Any]:
    with open(str(path), mode="rb") as fp:
        return load_toml_fp(fp)


def load_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as json_fp:
        return json.load(json_fp)


def is_eopf_adf_loaded(path_or_pattern: Any) -> bool:
    """

    :param path_or_pattern:
    :return:
    """
    return is_eopf_adf(path_or_pattern) and path_or_pattern.data_ptr is not None


def _cleaned_kwargs(kwargs: Any) -> dict[str, Any]:
    cleaned = {}
    for kwarg in kwargs:
        if kwarg not in stb_open_parameters:
            cleaned[kwarg] = kwargs[kwarg]
    return cleaned


def fix_kwargs_for_lazy_loading(kwargs: Any) -> None:
    if "chunks" not in kwargs:
        kwargs["chunks"] = {}
    else:
        if kwargs["chunks"] is None:
            raise ValueError(
                "open_datatree(chunks=None) is not allowed. Use load_datatree instead to avoid lazy loading data",
            )


def decode_storage_attributes(variable: Any, encoding: dict[str, Any] | None = None, path: str = "") -> dict[Any, Any]:
    if encoding is None:
        try:
            encoding = variable.encoding
        except AttributeError:
            encoding = {}
    io = {}
    attrs = {}
    fill_value = encoding.get("_FillValue", encoding.get("fill_value", -1))
    storage_type = encoding.get("dtype", encoding.get("storage_type", np.int32))
    defaults = dict(scale_factor=1.0, add_offset=0.0)
    zattrs = copy.copy(variable.attrs)

    for field in {
        "valid_min",
        "valid_max",
        "scale_factor",
        "add_offset",
    }:
        if field in zattrs:
            io[field] = zattrs[field]
        elif field in encoding:
            io[field] = encoding[field]
        elif field in defaults:
            io[field] = defaults[field]

    if fill_value is not None:
        io["fill_value"] = fill_value
    io["dtype"] = storage_type
    # Compute decode information
    scale_factor = io.get("scale_factor", 1.0)
    add_offset = io.get("add_offset", 0.0)
    mini = io.get("valid_min")
    maxi = io.get("valid_max")
    try:
        valid_max = (add_offset + maxi * scale_factor) if maxi is not None else None
    except TypeError:
        raise TypeError(
            f"{path}: TypeError during operation {add_offset=} + {maxi=} * {scale_factor=}",
        )
    try:
        valid_min = (add_offset + mini * scale_factor) if mini is not None else None
    except TypeError:
        raise TypeError(
            f"{path}: TypeError during operation {add_offset=} + {mini=} * {scale_factor=}",
        )
    decoded: dict[Hashable, Any] = {}
    decoded["valid_min"] = valid_min
    decoded["valid_max"] = valid_max

    # decoded["fill_value"] = np.iinfo(np.int32).min
    for field in {"valid_min", "valid_max"}:
        if decoded[field] is not None:
            attrs[field] = decoded[field]
    if io:
        attrs["_io_config"] = io

    # attrs["dtype"] = variable.dtype
    return attrs
