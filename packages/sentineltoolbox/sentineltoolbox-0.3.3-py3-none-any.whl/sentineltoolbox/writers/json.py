import logging
from typing import Any

from zarr import MemoryStore
from zarr.attrs import Attributes

logger = logging.getLogger("sentineltoolbox")


def serialize_to_zarr_json(log_data: Any, **kwargs: Any) -> Any:
    store = MemoryStore()
    attrs = Attributes(store)
    errors = kwargs.get("errors", "strict")
    try:
        attrs[""] = log_data
    except TypeError as e:
        if errors == "replace":
            # eschalk: call your code "to_json_best_effort" here
            # and recall serialize_to_zarr(jsonified, errors="strict") to be sure jsonified code
            # can be serialized with zarr
            logger.warning(f"serialize_to_zarr_json(data, {errors=!r}) not implemented yet, equivalent to 'ignore'")
            return repr(log_data)
        elif errors == "ignore":
            logger.warning(f"Cannot log data of type {type(log_data)!r}. replace by 'repr' str to keep information")
            return repr(log_data)
        else:
            logger.warning(f"Cannot log data of type {type(log_data)!r}. zarr cannot serialize it.")
            raise e
    else:
        return log_data
