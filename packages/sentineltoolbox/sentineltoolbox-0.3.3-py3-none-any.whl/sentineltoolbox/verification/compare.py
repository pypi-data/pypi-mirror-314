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
from typing import Any

import dask.array as da
import datatree
import numpy as np
import pandas as pd
import xarray as xr

from sentineltoolbox.filesystem_utils import get_fsspec_filesystem
from sentineltoolbox.readers.datatree_subset import filter_datatree

try:
    import matplotlib.pyplot as plt
    from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
except ImportError:
    PLOT_AVAILABLE = False
else:
    PLOT_AVAILABLE = True

logger = logging.getLogger("sentineltoolbox.verification")


# Formatted string when test fails
def _get_failed_formatted_string_vars(
    name: str,
    values: list[Any],
    threshold: float,
    relative: bool = True,
) -> str:
    if relative:
        return (
            f"{name}: "
            f"min={values[0]*100:8.4f}%, "
            f"max={values[1]*100:8.4f}%, "
            f"mean={values[2]*100:8.4f}%, "
            f"stdev={values[3]*100:8.4f}% "
            f"median={values[4]*100:8.4f}% "
            f"mse={values[5]:9.6f} "
            f"psnr={20 * np.log10(values[6]/values[5]):9.6f}dB -- "
            f"eps={threshold*100}% "
            f"outliers={values[7]} ({values[7]/values[-2]*100:5.2f}%) "
            f"samples={values[-2]}/{values[-1]}({values[-2]/values[-1]*100:5.2f}%)"
        )
    else:
        return (
            f"{name}: "
            f"min={values[0]:9.6f}, "
            f"max={values[1]:9.6f}, "
            f"mean={values[2]:9.6f}, "
            f"stdev={values[3]:9.6f} "
            f"median={values[4]:9.6f} "
            f"mse={values[5]:9.6f} "
            f"psnr={20 * np.log10(values[6]/values[5]):9.6f}dB -- "
            f"eps={threshold} "
            f"outliers={values[7]} ({values[7]/values[-2]*100:5.2f}%) "
            f"samples={values[-2]}/{values[-1]}({values[-2]/values[-1]*100:5.2f}%)"
        )


def _get_failed_formatted_string_flags(
    name: str,
    ds: xr.Dataset,
    bit: int,
    eps: float,
) -> str:
    return (
        f"{name} ({ds.bit_position.data[bit]})({ds.bit_meaning.data[bit]}): "
        f"equal_pix={ds.equal_percentage.data[bit]:8.4f}%, "
        f"diff_pix={ds.different_percentage.data[bit]:8.4f}% -- "
        f"eps={eps:8.4f}% "
        f"outliers={ds.different_count.data[bit]} "
        f"samples=({ds.total_bits.data[bit]})"
    )


def _get_passed_formatted_string_flags(name: str, ds: xr.Dataset, bit: int) -> str:
    return f"{name} ({ds.bit_position.data[bit]})({ds.bit_meaning.data[bit]})"


# Function to get leaf paths
def get_leaf_paths(paths: list[str]) -> list[str]:
    """Given a list of tree paths, returns leave paths

    Parameters
    ----------
    paths
        list of tree structure path

    Returns
    -------
        leaf paths
    """
    leaf_paths = []
    for i in range(len(paths)):
        if i == len(paths) - 1 or not paths[i + 1].startswith(paths[i] + "/"):
            leaf_paths.append(paths[i])
    return leaf_paths


def sort_datatree(tree: datatree.DataTree[Any]) -> datatree.DataTree[Any]:
    """Alphabetically sort datatree.DataTree nodes by tree name

    Parameters
    ----------
    tree
        input `datatree.DataTree`

    Returns
    -------
        Sorted `datatree.DataTree`
    """
    paths = tree.groups
    sorted_paths = sorted(paths)

    if tuple(sorted_paths) == paths:
        logger.debug(f"No need to sort {tree.name}")
        return tree
    else:
        logger.debug(f"Sorting {tree.name}")
        sorted_tree: datatree.DataTree[Any] = datatree.DataTree()
        sorted_paths = get_leaf_paths(sorted_paths)
        for p in sorted_paths[1:]:
            sorted_tree[p] = tree[p]

        sorted_tree.attrs.update(tree.attrs)
        return sorted_tree


def encode_time_dataset(ds: xr.Dataset) -> xr.Dataset:
    for name, var in ds.data_vars.items():
        if var.dtype == np.dtype("timedelta64[ns]") or var.dtype == np.dtype(
            "datetime64[ns]",
        ):
            ds[name] = var.astype(int)
    return ds


def encode_time_datatree(dt: datatree.DataTree[Any]) -> datatree.DataTree[Any]:
    for tree in dt.subtree:
        for name, var in tree.data_vars.items():
            if var.dtype == np.dtype("timedelta64[ns]") or var.dtype == np.dtype(
                "datetime64[ns]",
            ):
                tree[name] = var.astype(int)
        for name, coord in tree.coords.items():
            if coord.dtype == np.dtype("timedelta64[ns]") or coord.dtype == np.dtype(
                "datetime64[ns]",
            ):
                tree[name] = coord.astype(int)
                # tree[name].drop_duplicates(name)
    return dt


@datatree.map_over_subtree
def encode_time(ds: xr.Dataset) -> xr.Dataset:
    for name, var in ds.data_vars.items():
        if var.dtype == np.dtype("timedelta64[ns]") or var.dtype == np.dtype(
            "datetime64[ns]",
        ):
            ds[name] = var.astype(int)
    return ds


@datatree.map_over_subtree
def drop_duplicates(ds: xr.Dataset) -> xr.Dataset:
    """Drop duplicate values

    Parameters
    ----------
    ds
        input `xarray.Dataset` or `datatree.DataTree`

    Returns
    -------
        `xarray.Dataset` or `datatree.DataTree`
    """
    return ds.drop_duplicates(dim=...)


@datatree.map_over_subtree
def count_outliers(err: xr.Dataset, threshold: float) -> xr.Dataset:
    """For all variables of a `xarray.Dataset/datatree.DataTree`, count the number of outliers, exceeding the
    threshold value

    Parameters
    ----------
    err
        input `xarray.Dataset` or `datatree.DataTree`
    threshold
        Threshold value

    Returns
    -------
        reduced count `xarray.Dataset` or `datatree.DataTree`
    """
    return err.where(abs(err) >= threshold, np.nan).count(keep_attrs=True)


@datatree.map_over_subtree
def drop_coordinates(ds: xr.Dataset) -> xr.Dataset:
    """Remove all coordinates of a `datatree.DataTree

    Parameters
    ----------
    ds
        input `xarray.Dataset` or `datatree.DataTree`

    Returns
    -------
        `xarray.Dataset` or `datatree.DataTree`
    """
    return ds.drop_vars(ds.coords)


def compute_array_median(array: xr.DataArray) -> xr.DataArray:
    """Compute the median of a DataArray.
    It excludes NaN and it accounts for dask.array in which case the array
    needs to be explicitely flatten first

    Parameters
    ----------
    array
        input xr.DataArray

    Returns
    -------
        reduced DataArray with median
    """
    if isinstance(array.data, da.core.Array):
        return da.nanmedian(da.ravel(array), axis=0)
    else:
        return array.median(skipna=True)


@datatree.map_over_subtree
def compute_median(ds: xr.Dataset) -> xr.Dataset:
    """Compute the median of a DataTree, excluding NaN

    Parameters
    ----------
    ds
        input xr.Dataset

    Returns
    -------
        reduced Dataset with median
    """

    median_dict = {var: compute_array_median(ds[var]) for var in ds}
    return xr.Dataset(median_dict)


def _compute_reduced_datatree(tree: datatree.DataTree[Any], results: dict[str, Any] | None = None) -> dict[str, Any]:
    if not results:
        results = {}

    for tree in tree.subtree:
        for name, var in tree.variables.items():
            key = "/".join([tree.path, str(name)])
            if key in results:
                results[key].append(var.compute().data)
            else:
                results[key] = [var.compute().data]
            # results[name]=[var.compute().data]

    return results


def _get_coverage(tree: datatree.DataTree[Any], results: dict[str, Any] | None = None) -> dict[str, Any]:
    if not results:
        results = {}

    for tree in tree.subtree:
        for name, var in tree.variables.items():
            key = "/".join([tree.path, str(name)])
            if key in results:
                results[key].append(var.size)
                results[key].append(np.prod(var.shape))
            else:
                results[key] = [var.size, np.prod(var.shape)]

    return results


def variables_statistics(
    dt: datatree.DataTree[Any],
    dt_ref: datatree.DataTree[Any],
    relative: bool,
    threshold: float,
) -> tuple[dict[str, Any], datatree.DataTree[Any]]:
    """Compute statistics on all the variables of a `datatree.DataTree`
    Note that this function triggers the `dask.array.compute()`

    Parameters
    ----------
    dt
        input datatree
    threshold
        Threshold to be used to count a number of outliers, especially in the case where `dt` represents
        an absolute or relative difference

    Returns
    -------
        A dictionary with keys the name of the variable (including its tree path) and the list a computed statistics
    """
    with xr.set_options(keep_attrs=True):
        diff = dt - dt_ref  # type: ignore
        if relative:
            dt_ref_tmp = dt_ref.where(dt_ref != 0)
            dt_tmp = dt.where(dt_ref != 0)
            err = (dt_tmp - dt_ref_tmp) / dt_ref_tmp
        else:
            err = diff

    err = filter_datatree(
        err,
        [],
        type="flags",
    )
    diff = filter_datatree(
        diff,
        [],
        type="flags",
    )

    min_dt = err.min(skipna=True)
    max_dt = err.max(skipna=True)
    mean_dt = err.mean(skipna=True)
    std_dt = err.std(skipna=True)
    med_dt = compute_median(err)
    count = count_outliers(err, threshold)
    # Add new metrics mse and psnr
    mse = (diff * diff).mean(skipna=True)  # type: ignore
    sq_max_value = ((diff + dt_ref).max(skipna=True) - (diff + dt_ref).min(skipna=True)) ** 2

    results = _compute_reduced_datatree(min_dt)
    results = _compute_reduced_datatree(max_dt, results)
    results = _compute_reduced_datatree(mean_dt, results)
    results = _compute_reduced_datatree(std_dt, results)
    results = _compute_reduced_datatree(med_dt, results)
    results = _compute_reduced_datatree(mse, results)
    results = _compute_reduced_datatree(sq_max_value, results)
    results = _compute_reduced_datatree(count, results)
    # Coordinates are not accounted for after reduction operation as min,max...
    # So remove the coordintes from dt to get coverage
    results = _get_coverage(drop_coordinates(err), results)

    return results, err


def bitwise_statistics_over_dataarray(array: xr.DataArray) -> xr.Dataset:
    """Compute bitwise statistics over a dataarray

    Parameters
    ----------
    array
        input dataarray. It is assumed to represent the difference between 2 bitwise flag values for instance
        flag1 ^ flag2

    Returns
    -------
        returns a `xarray.dataset` indexed by the bit range with the following variables
        "bit_position",
        "bit_meaning",
        "total_bits":,
        "equal_count",
        "different_count",
        "equal_percentage",
        "different_percentage"
    """
    flag_meanings = array.attrs["flag_meanings"]
    mask = array.attrs.get("flag_masks", None)
    if mask is None:
        mask = array.attrs.get("flag_values")
    flag_masks = list(mask)

    # num_bits = len(flag_masks)
    key: list[str] = []
    if isinstance(flag_meanings, str):
        key = flag_meanings.split(" ")
    else:
        key = flag_meanings

    bit_stats: list[dict[str, Any]] = []

    for bit_mask in flag_masks:
        # get bit position aka log2(bit_mask)
        bit_pos = 0
        m = bit_mask
        while m > 1:
            m >>= 1
            bit_pos += 1
        # for bit_pos in range(num_bits):
        # bit_mask = 1 << bit_pos
        diff = (array & bit_mask) >> bit_pos
        equal_bits = diff == 0

        try:
            idx = flag_masks.index(bit_mask)
            # idx = np.where(flag_masks == bit_mask)
        except ValueError:
            print(
                f"Encounter problem while retrieving the bit position for value {bit_mask}",
            )

        flag_name = key[idx]

        total_bits = equal_bits.size
        equal_count = equal_bits.sum().compute().data
        diff_count = total_bits - equal_count

        bit_stats.append(
            {
                "bit_position": bit_pos,
                "bit_meaning": flag_name,
                "total_bits": total_bits,
                "equal_count": equal_count,
                "different_count": diff_count,
                "equal_percentage": equal_count / total_bits * 100,
                "different_percentage": diff_count / total_bits * 100,
            },
        )

    return xr.Dataset.from_dataframe(pd.DataFrame(bit_stats))


def bitwise_statistics(dt: datatree.DataTree[Any]) -> dict[str, xr.Dataset]:
    """Compute bitwise statistics on all the variables of a `datatree.DataTree`.
    The variables should represent flags/masks variables as defined by the CF conventions, aka including
    "flags_meanings" and "flags_values" as attributes
    Note that this function triggers the `dask.array.compute()`

    Parameters
    ----------
    dt
        input `datatree.DataTree

    Returns
    -------
        dictionary of `xarray.Dataset` with keys being the variable name.
        The `xarray.Dataset` is indexed by the bit range and contains the following variables
        "bit_position",
        "bit_meaning",
        "total_bits":,
        "equal_count",
        "different_count",
        "equal_percentage",
        "different_percentage"
    """
    # TODO test if dt only contains flags variables
    # call to filter_flags for instance

    res: dict[str, xr.Dataset] = {}
    for tree in dt.subtree:
        # if tree.is_leaf:
        if tree.ds:
            for var in tree.data_vars:
                res[var] = bitwise_statistics_over_dataarray(tree.data_vars[var])

    return res


def compute_confusion_matrix_for_dataarray(
    reference: xr.DataArray,
    predicted: xr.DataArray,
    normalize: Any | None = None,
    title: str | None = None,
    show: bool = False,
) -> float:
    """Display the confusion matrix for an array of exclusive flags

    Parameters
    ----------
    reference : xr.DataArray
        _description_
    predicted : xr.DataArray
        _description_
    normalize : Any | None, optional
        _description_, by default None
    title : str | None, optional
        _description_, by default None
    """
    if show and not PLOT_AVAILABLE:
        logger.warning("Please install sentineltoolbox extra-dependencies [dev] to display matrices.")
        logger.warning("Display matrix feature disabled")
        show = False
    true_1d = reference.values.ravel()
    pred_1d = predicted.values.ravel()

    unique_class_indices = list(set(np.unique(true_1d)) | set(np.unique(pred_1d)))
    labels = predicted.attrs["flag_meanings"]
    display_labels = [labels[i] for i in unique_class_indices]
    matrix = confusion_matrix(true_1d, pred_1d, normalize=normalize)
    if show:
        disp = ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=display_labels)
        disp.plot()
        plt.show()
    matrix_abs = confusion_matrix(true_1d, pred_1d)
    if show:
        disp = ConfusionMatrixDisplay(confusion_matrix=matrix_abs, display_labels=display_labels)
        disp.plot()
        plt.show()

    score = np.sum(np.diagonal(matrix_abs) * np.diagonal(matrix) * 100) / np.trace(matrix_abs)

    return score


def product_exists(input_path: str, secret: str | None = None) -> bool:
    """Check if input product exists wheter it is on filesystem or object-storage"""
    kwargs = {}
    if secret:
        kwargs["secret_alias"] = secret
    fs, url = get_fsspec_filesystem(input_path, **kwargs)
    return fs.exists(url)


def parse_cmp_vars(reference: str, new: str, cmp_vars: str) -> list[tuple[str, str]]:
    """Parse command-line option cmp-vars"""
    list_prods: list[tuple[str, str]] = []

    for vars in cmp_vars.split(","):
        var = vars.split(":")
        if len(var) != 2:
            raise ValueError(f"{cmp_vars} is not a valid --cmp-var option syntax")
        list_prods.append(
            (var[0], var[1]),
        )

    return list_prods


def get_threshold_from_scale_factor(dt: datatree.DataTree[Any], relative: bool, threshold: float) -> dict[str, float]:
    scaled_threshold = {}
    for tree in dt.subtree:
        for name, var in tree.variables.items():
            key = "/".join([tree.path, str(name)])
            scale_factor = var.encoding.get("scale_factor", None)
            if scale_factor and not relative:
                scaled_threshold[key] = scale_factor * 1.5
            else:
                scaled_threshold[key] = threshold

    return scaled_threshold
