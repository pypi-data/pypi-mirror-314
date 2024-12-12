# Copyright 2024 ACRI-ST
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys
from io import TextIOWrapper
from typing import Any, TextIO

import click
import datatree
import numpy as np
import xarray as xr

from sentineltoolbox.readers.datatree_subset import filter_datatree, filter_flags
from sentineltoolbox.readers.open_datatree import open_datatree
from sentineltoolbox.verification.compare import (
    _get_failed_formatted_string_flags,
    _get_failed_formatted_string_vars,
    _get_passed_formatted_string_flags,
    bitwise_statistics,
    compute_confusion_matrix_for_dataarray,
    get_threshold_from_scale_factor,
    parse_cmp_vars,
    product_exists,
    sort_datatree,
    variables_statistics,
)
from sentineltoolbox.verification.logger import (
    get_failed_logger,
    get_logger,
    get_passed_logger,
)


def compare_products(
    reference: str,
    actual: str,
    cmp_vars: str | None = None,
    cmp_grps: str | None = None,
    verbose: bool = False,
    info: bool = False,
    relative: bool = False,
    threshold: float = 1.0e-6,
    threshold_flags: float = 1.0e-2,
    flags_only: bool = False,
    secret: str | None = None,
    output: str | None = None,
    **kwargs: Any,
) -> (
    tuple[datatree.DataTree[Any] | None, datatree.DataTree[Any] | None, float | None, list[float] | None] | RuntimeError
):
    """Compare two products Zarr or SAFE.

    Parameters
    ----------
    reference: Path
        Reference product path
    actual: Path
        New product path
    verbose: bool
        2-level of verbosity (INFO or DEBUG)
    relative: bool
        Compute relative or absolute error, default is True
    threshold
        Threshold to determine wheter the comparison is PASSED or FAILED
    """
    # Initialize stream
    stream: TextIOWrapper | TextIO
    if output:
        stream = open(output, mode="w")
    else:
        stream = sys.stderr

    # Initialize logging
    level = logging.INFO
    if verbose:
        level = logging.DEBUG
    logger = get_logger("compare", level=level, stream=stream)
    logger.setLevel(level)

    passed_logger = get_passed_logger("passed", stream=stream)
    failed_logger = get_failed_logger("failed", stream=stream)

    # Check input products
    if not product_exists(reference, secret=secret):
        logger.error(f"{reference} cannot be found.")
        exit(1)
    if not product_exists(actual, secret=secret):
        logger.error(f"{actual} cannot be found.")
        exit(1)
    logger.info(
        f"Compare the new product {actual} to the reference product {reference}",
    )

    # Check if specific variables
    if cmp_vars:
        list_ref_new_vars = parse_cmp_vars(reference, actual, cmp_vars)
    if cmp_grps:
        list_ref_new_grps = parse_cmp_vars(reference, actual, cmp_grps)

    kwargs["decode_times"] = False
    if secret:
        kwargs["secret_alias"] = secret
    # Open reference product
    dt_ref = open_datatree(reference, **kwargs)
    dt_ref.name = "ref"
    logger.debug(dt_ref)

    # Open new product
    dt_new = open_datatree(actual, **kwargs)
    dt_new.name = "new"
    logger.debug(dt_new)

    # Sort datatree
    dt_ref = sort_datatree(dt_ref)
    dt_new = sort_datatree(dt_new)

    # Get product type
    eopf_type = dt_ref.attrs["stac_discovery"]["properties"].get("eopf:type", None)

    # Filter datatree
    if cmp_vars:
        dt_ref = filter_datatree(
            dt_ref,
            [var[0] for var in list_ref_new_vars],
            type="variables",
        )
        dt_new = filter_datatree(
            dt_new,
            [var[1] for var in list_ref_new_vars],
            type="variables",
        )
    if cmp_grps:
        dt_ref = filter_datatree(
            dt_ref,
            [var[0] for var in list_ref_new_grps],
            type="groups",
        )
        dt_new = filter_datatree(
            dt_new,
            [var[1] for var in list_ref_new_grps],
            type="groups",
        )

    # Check if datatrees are isomorphic
    if not dt_new.isomorphic(dt_ref):
        logger.error("Reference and new products are not isomorphic")
        logger.error("Comparison fails")
        raise RuntimeError

    # Variable statistics
    score: float | None = 0
    if not flags_only:
        results, err = variables_statistics(dt_new, dt_ref, relative, threshold)

        scaled_threshold: dict[str, float] = get_threshold_from_scale_factor(dt_ref, relative, threshold)
        logger.info("-- Verification of variables")
        for name, val in results.items():
            if name.endswith("spatial_ref") or name.endswith("band"):
                continue
            thresh = scaled_threshold.get(name, threshold)
            if all(np.abs(v) < thresh for v in val[:3]):
                if info:
                    passed_logger.info(
                        _get_failed_formatted_string_vars(
                            name,
                            val,
                            thresh,
                            relative=relative,
                        ),
                    )
                else:
                    passed_logger.info(f"{name}")
            else:
                failed_logger.info(
                    _get_failed_formatted_string_vars(
                        name,
                        val,
                        thresh,
                        relative=relative,
                    ),
                )

        # Global scoring:
        if relative:
            score = 100.0 - np.abs(np.nanmedian([np.abs((res[2] + res[4]) * 0.5) for res in results.values()]) * 100)
            logger.debug(
                """Metrics is: 100% - |median_over_variables(0.5 * (
                                    (1 / npix) *sum_npix(err_rel[p]) + median_pix(err_rel[p])
                                    ) * 100|

                        with err_rel[p] = (val[p] - ref[p]) / ref[p]
                        """,
            )
            logger.info(f"   Global scoring for non-flag variables = {score:20.12f}%")
        else:
            # # score = np.median([(res[2] + res[4] + np.max([0, 1 - res[6] / 30])) / 3 for res in results.values()])
            # score = np.median([(res[2] + res[4]) / 2 for res in results.values()])
            # logger.debug(
            #     # """Metrics is: median_over_variables( 1/3 * (
            #     #             (1 / npix) *sum_npix(err[p]) + median_pix(err[p]) + max(0,1-psnr/30)
            #     """Metrics is: median_over_variables( 1/2 * (
            #                 (1 / npix) *sum_npix(err[p]) + median_pix(err[p])
            #                         )

            #             with err[p] = val[p] - ref[p]
            #             """,
            # )
            # logger.info(f"   Global precision for non-flag variables is = {score:20.12f}")
            score = None
    else:
        err = None

    # Flags statistics
    flags_ref = filter_flags(dt_ref)
    flags_new = filter_flags(dt_new)

    # Patch for S2 L2
    # Attributes for reference product are not correct so that filtering flags is ineffective
    # TODO: for exclusive flags (detected on attributes=flag_values), use the confusion matrix
    # instead of the bitwise statistics which is not correct
    try:
        if eopf_type in [
            "S02MSIL1C",
            "S02MSIL2A",
        ]:
            patch_s2l2 = True
        else:
            patch_s2l2 = False
    except KeyError:
        patch_s2l2 = False

    score_flag: list[float] = []
    if patch_s2l2:
        score_flag_scl = compute_confusion_matrix_for_dataarray(
            dt_ref.conditions.mask.l2a_classification.r20m.scl,
            dt_new.conditions.mask.l2a_classification.r20m.scl,
            normalize="true",
        )
        score_flag.append(score_flag_scl)
        err_flags = None
        logger.info(f"   Score for scene classification is = {score_flag[0]}")
    else:
        try:
            with xr.set_options(keep_attrs=True):
                err_flags = flags_ref ^ flags_new
        except TypeError:
            pass
        else:
            res: dict[str, xr.Dataset] = bitwise_statistics(err_flags)
            eps = 100.0 * (1.0 - threshold_flags)
            logger.info(f"-- Verification of flags: threshold = {eps}%")
            for name, ds in res.items():
                # ds_outlier = ds.where(ds.equal_percentage < eps, other=-1, drop=True)
                for bit in ds.index.data:
                    if ds.equal_percentage[bit] < eps:
                        failed_logger.info(
                            _get_failed_formatted_string_flags(name, ds, bit, eps),
                        )
                    else:
                        passed_logger.info(
                            _get_passed_formatted_string_flags(name, ds, bit),
                        )

        # Global scoring for flags
        # score_flag: list[float] = []
        for name, ds in res.items():
            score_var: float = 0
            sum_weight: float = 0
            for bit in ds.index.data:
                weight = ds.equal_count.data[bit] + ds.different_count.data[bit]
                sum_weight += weight
                score_var = score_var + ds.equal_percentage.data[bit] * weight
            score_var /= sum_weight
            score_flag.append(score_var)

        logger.info(f"   Scores for flag variables are = {score_flag}")
        logger.info(f"   Global scores for flag variables is = {np.nanmedian(score_flag)   :20.12f}")

    logger.info("Exiting compare")

    if output:
        stream.close()

    return err, err_flags, score, score_flag


@click.command()
@click.argument("reference", type=str, nargs=1, required=True)
@click.argument("actual", type=str, nargs=1, required=True)
@click.option(
    "--cmp-vars",
    type=str,
    help="Compare only specific variables, defined as: path/to/var_ref:path/to/var_new,... ",
)
@click.option(
    "--cmp-grps",
    type=str,
    help="Compare only specific groups, defined as: path/to/grp_ref:path/to/grp_new,... ",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    show_default=True,
    help="increased verbosity",
)
@click.option(
    "--info",
    is_flag=True,
    default=False,
    show_default=True,
    help="always display statistics even if PASSED",
)
@click.option(
    "--relative",
    is_flag=True,
    default=False,
    show_default=True,
    help="Compute relative error",
)
@click.option(
    "--threshold",
    required=False,
    type=float,
    default=1.0e-6,
    show_default=True,
    help="Error Threshold defining the PASSED/FAILED result",
)
@click.option(
    "--threshold-flags",
    required=False,
    type=float,
    default=1.0e-2,
    show_default=True,
    help="Flag Threshold defining the PASSED/FAILED result",
)
@click.option(
    "--flags-only",
    required=False,
    is_flag=True,
    default=False,
    show_default=True,
    help="Compute comparison only for flags/masks variables",
)
@click.option(
    "-s",
    "--secret",
    required=False,
    show_default=True,
    help="Secret alias if available extracted from env. variable S3_SECRETS_JSON_BASE64 or in /home/.eopf/secrets.json",
)
@click.option("-o", "--output", required=False, help="output file")
def compare(
    reference: str,
    actual: str,
    cmp_vars: str,
    cmp_grps: str,
    verbose: bool,
    info: bool,
    relative: bool,
    threshold: float,
    threshold_flags: float,
    flags_only: bool,
    secret: str,
    output: str,
    **kwargs: Any,
) -> None:
    """CLI tool to compare two products Zarr or SAFE.

    Parameters
    ----------
    reference: Path
        Reference product path
    actual: Path
        New product path
    verbose: bool
        2-level of verbosity (INFO or DEBUG)
    relative: bool
        Compute relative or absolute error, default is True
    threshold
        Threshold to determine wheter the comparison is PASSED or FAILED
    """
    compare_products(
        reference,
        actual,
        cmp_vars=cmp_vars,
        cmp_grps=cmp_grps,
        verbose=verbose,
        info=info,
        relative=relative,
        threshold=threshold,
        threshold_flags=threshold_flags,
        flags_only=flags_only,
        secret=secret,
        output=output,
        **kwargs,
    )
