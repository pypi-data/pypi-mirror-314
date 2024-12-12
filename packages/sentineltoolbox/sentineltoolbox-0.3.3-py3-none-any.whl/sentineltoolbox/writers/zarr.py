from typing import Any

from datatree import DataTree


def write_zarr(xdt: DataTree[Any], path: Any, **kwargs: Any) -> None:
    xdt.to_zarr(str(path))
