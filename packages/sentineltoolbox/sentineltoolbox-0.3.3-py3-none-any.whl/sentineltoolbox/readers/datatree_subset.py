from typing import Any, Literal

import datatree
import xarray as xr


@datatree.map_over_subtree
def filter_flags(ds: xr.Dataset) -> xr.Dataset:
    """Filter only flags variable while preserving the whole structure
    Following the CF convention, flag variables are filtered based on the presence of "flag_masks" attribute

    Parameters
    ----------
    ds
        input xarray.Dataset or datatree.DataTree

    Returns
    -------
        xarray.Dataset or datatree.DataTree
    """
    return xr.merge(
        [
            ds.filter_by_attrs(flag_masks=lambda v: v is not None),
            ds.filter_by_attrs(flag_values=lambda v: v is not None),
        ],
    )


def filter_datatree(
    dt: datatree.DataTree[Any],
    vars_grps: list[str],
    type: Literal["variables", "groups", "flags"],
) -> datatree.DataTree[Any]:
    """Filter datatree by selecting a list of given variables or groups

    Parameters
    ----------
    dt
        input datatree.DataTree
    vars_grps
        List of variable or group paths
    type
        Defines if the list is made of variables or groups ("variables" or "groups")

    Returns
    -------
        Filtered datatree.DataTree

    Raises
    ------
    ValueError
        if incorrect type is provided
    """
    if type == "variables":
        dt = dt.filter(
            lambda node: any(
                "/".join([node.path, var]) in vars_grps for var in node.variables  # type: ignore[list-item]
            ),
        )
        for tree in dt.subtree:
            grp = tree.path
            variables = list(tree.data_vars)
            drop_variables = [v for v in variables if "/".join([grp, v]) not in vars_grps]
            if drop_variables:
                dt[grp] = dt[grp].drop_vars(drop_variables)
    elif type == "groups":
        dt = dt.filter(
            lambda node: next((s for s in node.groups if s in vars_grps), False),
        )
    elif type == "flags":
        for tree in dt.subtree:
            grp = tree.path
            variables = list(tree.data_vars)
            drop_variables = [v for v in variables if "flag_masks" in tree[v].attrs or "flag_values" in tree[v].attrs]
            if drop_variables:
                dt[grp] = dt[grp].drop_vars(drop_variables)
    else:
        raise ValueError("type as incorrect value: ", type)

    return dt
