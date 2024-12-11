from typing import Tuple

import xarray as xr

from mfire.localisation.area_algebra import compute_iol_left, compute_iou
from mfire.settings import N_CUTS, SPACE_DIM, TIME_DIM, get_logger
from mfire.utils.exception import LocalisationError, LocalisationWarning

# Logging
LOGGER = get_logger(name="modal_localisation", bind="iolulocalisation")

# minimal risk density required in a zone to be select after the first
DENSITY_THRESHOLD = 0.2


def best_zone(
    areas: xr.DataArray, risk_da: xr.DataArray
) -> Tuple[xr.DataArray, xr.DataArray, float]:
    """
    Select the best zone in a list, using both IoL and IoU metrics.

    Args:
        areas: An xarray DataArray with the area data.
        risk_da: An xarray DataArray with the risk data.
        space_dim: The dimension of the spatial coordinates.
        time_dim: The dimension of the time coordinates.

    Returns:
        best_area: An xarray DataArray with the best zone.
        iol_zone: The IoL metric of the best zone.
        max_iol: The maximum IoL metric of all the zones.
    """

    # Sort the risk data array by latitude, to prevent exceptions.
    risk_da = risk_da.reindex(latitude=sorted(risk_da.latitude))
    areas = areas.reindex(latitude=sorted(areas.latitude))

    # Select the zones with the highest IoL.
    iol_sum = compute_iol_left(areas, risk_da, SPACE_DIM).sum(TIME_DIM)
    # 0.90 to 0.75 in order to get largest zones (perhaps domain)
    best_iol_quantile = areas.where(iol_sum >= iol_sum.quantile(0.75), drop=True)
    best_iol_max = areas.where(iol_sum > iol_sum.max() * 0.75, drop=True)

    # If there are more zones in the best_iol_quantile group than in the
    # best_iol_max group, then select the best_iol_quantile group. Otherwise,
    # select the best_iol_max group.
    if best_iol_quantile.count() > best_iol_max.count():
        best_iol = best_iol_quantile
    else:
        best_iol = best_iol_max

    # Select the zone with the highest IoU.
    var_da = compute_iou(risk_da, best_iol, SPACE_DIM).sum(TIME_DIM)
    var_argmax = var_da.argmax()

    # Keep only the very best zone.
    best_area = best_iol.isel(id=var_argmax)

    # making up
    best_area = best_area.expand_dims(dim={"id": 1})
    best_area = best_area.assign_coords(
        id=best_area.id,
        areaName=("id", [str(best_area.areaName.values)]),
        altAreaName=("id", [str(best_area.altAreaName.values)]),
        areaType=("id", [str(best_area.areaType.values)]),
    )

    # Calculate the maximum IoL metric of all the zones and IoL metric of the best zone.
    max_iol = compute_iol_left(areas, risk_da, SPACE_DIM).max().data
    iol = compute_iol_left(best_area, risk_da, SPACE_DIM).max(TIME_DIM)
    return best_area, iol, max_iol


def _get_n_area_loop(
    areas, area, time_sel, remaining_risk
) -> Tuple[xr.DataArray, xr.DataArray, bool]:
    best_area, iol, max_iol = best_zone(areas, remaining_risk)

    # If the best zone covers the entire axis, switch to a single zone.
    if best_area.id == area.id:
        raise LocalisationWarning("The whole zone is the best localisation")

    # Remove the best zone from the list of available zones.
    areas = areas.where(areas.id != best_area.id.values, drop=True)

    # After the first zone, only keep the zones that are large enough.
    if len(time_sel) == 0 or iol > DENSITY_THRESHOLD:
        remaining_risk = (remaining_risk - best_area.isel(id=0).fillna(0)).mask.f32
        time_sel.append(best_area)
        return areas, remaining_risk, remaining_risk.count() > 0

    # If all the zones have low risk or there are no more zones available,
    # stop selecting zones.
    return (
        areas,
        remaining_risk,
        remaining_risk.count() > 0
        and max_iol >= DENSITY_THRESHOLD
        and areas.id.count() == 0,
    )


def get_n_area(
    risk_da: xr.DataArray, area: xr.DataArray, areas: xr.DataArray
) -> xr.DataArray:
    """
    Splits a given domain into n_cuts zones from areas_da

    Args:
        risk_da (xr.DataArray): Previously calculated risk.
        area (xr.DataArray): The zone defined as the domain.
        areas (xr.DataArray): The list of descriptive zones
            valid for splitting.
        n_cuts (int): Number of successive cuts. Defaults to N_CUTS.
        space_dim (Dimension): Spatial dimension(s).
            Defaults to SPACE_DIM.
        time_dim (Dimension): Temporal dimension(s).

    Raises:
        LocalisationWarning: Exception raised if it is impossible to perform a single
            domain split. This allows the Manager to take over.
        LocalisationError: Other error.

    Returns:
        xr.DataArray: DataArray containing the selected zones.
    """
    try:
        remaining_risk = risk_da.mask.f32
        time_sel = []

        # Add the domain to allow switching to monozone.
        areas = xr.concat([areas, area], dim="id")

        # Select at most n_cuts zones.
        while len(time_sel) < N_CUTS:
            areas, remaining_risk, continue_cutting = _get_n_area_loop(
                areas, area, time_sel, remaining_risk
            )
            if not continue_cutting:
                break

        return xr.concat(time_sel, dim="id")
    except (LocalisationWarning, LocalisationError):
        raise
    except Exception as excpt:
        raise LocalisationError(str(excpt)) from excpt
