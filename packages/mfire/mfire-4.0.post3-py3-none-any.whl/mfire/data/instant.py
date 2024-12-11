"""
instant data (as grib define)
concatenate
export to netcdf
and propose to other process
"""
from typing import List, Tuple

import numpy as np

from mfire.settings import get_logger
from mfire.utils import mfxarray as xr
from mfire.utils import xr as xr_utils

# Logging
LOGGER = get_logger(name=__name__)


def concatenate_and_preprocess(dict_das: dict) -> xr.DataArray:
    """
    Concatenates and preprocesses a dictionary of xarray DataArrays.
    for non-cumulative data
    Args:
        data_dict (Dict[str, Any]): A dictionary containing data for processing.
            It should include the following keys:

            - `files` (dict): A dictionary containing information about the input
              data files.
            - `postproc` (dict): A dictionary containing post-processing
              configurations, including:
                - `grid` (str): The target grid for regridding.
                - `param` (str): The desired variable name for the output.
                - `step` (int): The target time step (frequency) for the output
                  (e.g., hourly for "h").
                - `start` (str): The start date/time for slicing the output.
                - `stop` (str): The end date/time for slicing the output.

    Returns:
        xr.DataArray: The preprocessed and concatenated dataarray.
    """
    # Extract data and configurations
    source_file = dict_das["files"].values()
    target_variable_name = dict_das["postproc"]["param"]
    target_step = dict_das["postproc"]["step"]

    # Initialize variables
    target_grid = dict_das["postproc"]["grid"]
    concatenated = []
    source_steps = []

    # Loop through dataarrays, perform regridding if needed, and collect information
    for elt in sorted(source_file, key=lambda x: x["data"].valid_time.values):
        source_grid = elt["preproc"].get("source_grid")
        source_steps.append(int(elt["preproc"].get("source_step", 1)))
        if source_grid == target_grid:
            concatenated.append(elt["data"])
        else:
            LOGGER.info(f"Regridding data from {source_grid} to {target_grid}")
            da = xr_utils.interpolate_to_new_grid(elt["data"], target_grid)
            concatenated.append(da)

    # Concatenate dataarrays along the "valid_time" dimension
    concat_da = xr.concat(concatenated, dim="valid_time")

    # Sort by "valid_time"
    concat_da = concat_da.sortby("valid_time")

    # Set variable name
    concat_da.name = target_variable_name

    # Fill missing time steps if necessary
    if (np.array(source_steps) != target_step).any():
        LOGGER.info(
            "Source and target time steps differ, filling with xr_utils.fill_da",
            source_steps=source_steps,
            target_step=target_step,
            dim="valid_time",
        )
        concat_da = xr_utils.fill_da(
            da=concat_da,
            source_steps=source_steps,
            target_step=target_step,
            freq_base="h",
        )

    return xr_utils.slice_da(
        da=concat_da,
        start=dict_das["postproc"]["start"],
        stop=dict_das["postproc"]["stop"],
        coord_name="valid_time",
    )


def compute_instant(
    output_filename: str, dict_das: dict
) -> Tuple[List[bool], xr.DataArray, str, str]:
    """
    Parallel function
    Concatenates and exports a dictionary of xarray DataArrays to a NetCDF file.

    This function takes a dictionary mapping variable names to their corresponding
    DataArrays and concatenates them along a specific dimension (assumed to be
    consistent across all DataArrays). It then exports the resulting concatenated
    DataArray to a NetCDF file specified by `output_filename`.

    Args:
        output_filename (Path): The path to the output NetCDF file.
        dataarrays (Dict[str, xr.DataArray]): A dictionary containing xarray
            DataArrays to be concatenated. The key represents the variable name
            and the value is the corresponding DataArray.

    Returns:
        [bool]: True if the concatenation and export were successful, False otherwise.
        xr.DataArray: thre concatened data
        str: output_filename
        str: parametre
    """
    logger = LOGGER.bind(output_filename=output_filename)

    try:
        concat_da = concatenate_and_preprocess(dict_das=dict_das)
    except Exception:
        logger.error("Failed to concat", exc_info=True)
        return [False], None, None, None
    try:
        if concat_da.latitude[0] < concat_da.latitude[-1]:
            concat_da = concat_da.reindex(latitude=concat_da.latitude[::-1])
        concat_da = concat_da.assign_attrs({"PROMETHEE_z_ref": dict_das["grid"]})
        concat_da.to_netcdf(output_filename)
    except Exception:
        logger.error("Failed to export", exc_info=True)
        return [False], None, None, None
    return [True], concat_da, output_filename, dict_das["param"]
