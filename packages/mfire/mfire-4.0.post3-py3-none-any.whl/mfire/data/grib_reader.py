"""
Functions about grib file
"""
from typing import Dict, List, Tuple, Union

from mfire.configuration.rules import Rules
from mfire.settings import get_logger
from mfire.utils import exception
from mfire.utils import mfxarray as xr
from mfire.utils import xr as xr_utils

# Logging
LOGGER = get_logger(name=__name__)


grib_param_dtypes: dict = {
    "discipline": int,
    "parameterCategory": int,
    "productDefinitionTemplateNumber": int,
    "parameterNumber": int,
    "typeOfFirstFixedSurface": str,
    "level": int,
    "typeOfStatisticalProcessing": int,
    "derivedForecast": int,
    "percentileValue": int,
    "scaledValueOfLowerLimit": int,
    "scaledValueOfUpperLimit": int,
    "lengthOfTimeRange": int,
    "units": str,
}
mandatory_grib_param: list = [
    "subCentre",
    "dataTime",
    "name",
    "units",
    "startStep",
    "endStep",
    "stepRange",
]
optional_grib_param: list = ["dtype"]


def grib_params(rules: Rules, param: str, model: str) -> Dict[str, str]:
    """
    Retrieves GRIB parameter information for a specific rule,parameter and model.

    This method extracts a dictionary containing key-value pairs representing the
    GRIB parameter information associated with the provided `grib_param` and
    `model_name`. The parameter and model names should follow the Promethee standard
    defined in the 'RULES' CSV configuration file.

    Args:
        rules (Rules): to get  RULES csv standard
        param (str): Param's name following the Promethee standard
        model (str): Model's name following the Promethee standard

    Returns:
        Dict[str, str]: A dictionary containing key-value pairs of extracted GRIB
            parameter information, or an empty dictionary if information is not
            found.
    """
    try:
        # Select data for the specific grib_param and model_name
        return rules.grib_param_df.loc[(param, model)].dropna().to_dict()
    except KeyError:
        # Handle case where specific combination is not found
        LOGGER.warning(
            f"Combination ({param}, {model}) not found in grib_param_df. "
            f"Model 'default' is used to retrieve '{param}'."
        )
        return rules.grib_param_df.loc[(param, "default")].dropna().to_dict()


def backend_kwargs(
    rules: Rules, param: str, model: str
) -> Dict[str, Union[List[str], Dict[str, str], str]]:
    """
    Constructs the core backend keyword arguments dictionary for the cfgrib engine.

    This method retrieves the necessary configuration information from the internal
    GRIB parameter DataFrame and constructs a dictionary containing the core
    keyword arguments required by the `cfgrib` engine.

    Args:
        rules (Rules): to get  RULES csv standard
        param (str): The name of the GRIB parameter following the Promethee
            standard.
        name (str): The name of the model following the Promethee standard.

    Returns:
        Dict[str, Union[List[str], Dict[str, str]]]: A dictionary containing
            the core backend keyword arguments for the `cfgrib` engine.
    """

    raw_dico = grib_params(rules, param=param, model=model)
    # Extract and validate parameter keys and values
    param_keys = {}
    for key, value in raw_dico.items():
        if key in optional_grib_param:
            continue
        if key not in grib_param_dtypes:
            raise exception.ConfigurationError(
                f"Grib param key '{key}' not referenced in the grib_param_dtypes"
            )
        value_type = grib_param_dtypes[key]
        param_keys[key] = value_type(value)

    return {
        "read_keys": list(param_keys.keys()) + mandatory_grib_param,
        "filter_by_keys": param_keys,
        # to avoid ERROR
        "indexpath": "",
    }


def get_param_dtype(rules: Rules, param: str, model: str) -> str:
    """Gives the supposed dtype of a given param in the given model

    Args:
        rules (Rules): to get  RULES csv standard
        param (str): Param's name frollowing the Promethee standard (defined
            in the RULES csv configuration file)
        model (str): Model name following the Promethee standard (defined in
            the RULES csv standard)

    Returns:
        str: Expected dtype of the variable
    """
    return grib_params(rules, param=param, model=model).get("dtype", "float32")


def grib_filter(
    rules: Rules, param: str, model: str, step: int
) -> Tuple[dict, str, str]:
    """
    Retrieve info to select only one message in a grib
    Args:
        rules (Rules): to get  RULES csv standard
        param (str): Param's name frollowing the Promethee standard (defined
            in the RULES csv configuration file)
        model (str): Model name following the Promethee standard (defined in
            the RULES csv standard)

    Returns:
        backend_kwargs(dict): filter message info
        dtype (str): datatype expected
        units (str): unit expected

    """
    try:
        backend = backend_kwargs(rules, param, model)
        dtype = get_param_dtype(rules, param, model)
    except Exception:
        LOGGER.error(
            "Failed to retrieve backend_kwargs for (param, model)"
            f" = ({param}, {rules.name}).",
            exc_info=True,
        )
        raise

    # Case of a accum param with lengthOfTimeRange
    if "lengthOfTimeRange" in backend["filter_by_keys"]:
        backend["filter_by_keys"]["lengthOfTimeRange"] = int(step)

    units = backend["filter_by_keys"].pop("units", None)
    return backend, dtype, units


def load_single_grib_param(
    rules, file_id: Tuple, file_conf: dict
) -> Tuple[Tuple, xr.DataArray]:
    """
    Loads and processes a single parameter, step, and grid from a GRIB file. This
    function extracts the specified parameter from the provided GRIB file using
    the `cfgrib` engine.

    Args:
        rules (Rules): to get  RULES csv standard
        file_id (tuple): A tuple containing unique identification information
            for the file (details not shown here).
        file_config (dict): A dictionary containing configuration options for
            processing the GRIB file. It includes the following keys:

            - `grib_filename` (str): Name of the raw GRIB file.
            - param (str): Name of the param
            - model (str): nwp model producer
            - step : duration of the data
            - `grib_attrs` (dict): A dictionary containing attribute
                corrections to be applied to the extracted data.

    Returns:
        Tuple[tuple, xr.DataArray]: A tuple containing:

            - `file_id` (tuple): The original `file_id`.
            - `dataarray` (xr.DataArray): The extracted and processed data as a
              xarray DataArray.
    """
    dataarray = None
    # la valeur peut etre dans step ou term ( selon version)
    file_conf.setdefault(
        "step",
        file_conf.get(
            "backend_kwargs", {"filter_by_keys": {"lengthOfTimeRange": None}}
        )["filter_by_keys"]["lengthOfTimeRange"],
    )
    grib_args, dtype, units = grib_filter(
        rules, file_conf["param"], file_conf["model"], file_conf["step"]
    )
    file_conf["grib_attrs"] = {"units": units}
    log_kwargs = {
        "file_id": file_id,
        "grib_filename": file_conf["grib_filename"],
        "grib_filter": grib_args.get("filter_by_keys"),
        "func": "load_single_grib_param",
    }
    try:
        # Open dataarray with cfgrib engine and load data
        with xr.open_dataarray(
            file_conf["grib_filename"], engine="cfgrib", backend_kwargs=grib_args
        ) as tmp_da:
            dataarray = xr_utils.rounding(tmp_da.load())
    except Exception as e:
        LOGGER.error(f"Failed to extract parameter from file. {e}", **log_kwargs)
        return file_id, dataarray

    # Data type casting and handling potential errors
    try:
        if dtype in ["int8", "int16"]:
            dataarray = dataarray.fillna(0)
        dataarray = dataarray.astype(dtype)
    except TypeError as e:
        LOGGER.warning(
            f"Failed to cast dtype {dtype} to the extracted dataarray: {e}",
            **log_kwargs,
        )

    # Apply attribute corrections from configuration
    for attr_key, attr_value in file_conf["grib_attrs"].items():
        # Check if attribute exists and needs correction
        if dataarray.attrs.get(attr_key, "unknown") != attr_value:
            # Handle special case for 'units' attribute with logging
            if attr_key == "units" and attr_value is not None:
                LOGGER.debug(
                    f"Found 'units' = {dataarray.attrs[attr_key]} while '{attr_value}' "
                    f"expected. Changing 'units' to '{attr_value}'.",
                    **log_kwargs,
                )
            dataarray.attrs[attr_key] = attr_value
    # add "valid_time" dimension and set standard attributes
    dataarray = dataarray.expand_dims(dim={"valid_time": 1}, axis=0)
    dataarray["valid_time"] = dataarray.valid_time.assign_attrs(
        {"standard_name": "time", "long_name": "time"}
    )
    # clean some info
    var_to_delete = {"heightAboveGround", "time", "step", "surface"}
    drop_var = set(dataarray.coords).intersection(var_to_delete)
    dataarray = dataarray.drop_vars(list(drop_var))

    return file_id, dataarray
