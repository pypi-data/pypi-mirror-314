import json
import logging
from typing import Any

from sentineltoolbox.exceptions import LoadingDataError
from sentineltoolbox.filesystem_utils import get_url_and_credentials
from sentineltoolbox.readers._utils import is_eopf_adf_loaded
from sentineltoolbox.typedefs import Credentials, PathMatchingCriteria, PathOrPattern


def open_json(
    path_or_pattern: PathOrPattern,
    *,
    credentials: Credentials | None = None,
    match_criteria: PathMatchingCriteria = "last_creation_date",
    **kwargs: Any,
) -> dict[Any, Any]:
    if is_eopf_adf_loaded(path_or_pattern) and isinstance(path_or_pattern.data_ptr, dict):
        return path_or_pattern.data_ptr

    url, upath, credentials = get_url_and_credentials(
        path_or_pattern,
        credentials=credentials,
        match_criteria=match_criteria,
        **kwargs,
    )

    logger = kwargs.get("logger", logging.getLogger("sentineltoolbox"))
    logger.info(f"open {url}")

    try:
        with upath.open(mode="r", encoding="utf-8") as json_fp:
            return json.load(json_fp)
    except json.JSONDecodeError:
        raise LoadingDataError(url)


def load_json(
    path_or_pattern: PathOrPattern,
    *,
    credentials: Credentials | None = None,
    match_criteria: PathMatchingCriteria = "last_creation_date",
    **kwargs: Any,
) -> dict[Any, Any]:
    return open_json(path_or_pattern, credentials=credentials, match_criteria=match_criteria, **kwargs)
