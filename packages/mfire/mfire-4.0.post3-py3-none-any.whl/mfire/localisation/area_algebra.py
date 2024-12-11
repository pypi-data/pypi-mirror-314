from typing import Dict, List, Optional, Sequence, Union

import mfire.utils.mfxarray as xr
from mfire.localisation.altitude import AltitudeInterval
from mfire.settings import ALT_MAX, ALT_MIN, SPACE_DIM, Dimension, get_logger
from mfire.utils.string import _

__all__ = ["compute_iou"]

# Logging
LOGGER = get_logger(name="areaAlgebra", bind="areaAlgebra")

DEFAULT_IOU = 0.5
DEFAULT_IOU_ALT = 0.7  # Pour nommer une zone "spatiale" par une zone d'altitude


def compute_iou(
    left_da: xr.DataArray, right_da: xr.DataArray, dims: Dimension = SPACE_DIM
) -> xr.DataArray:
    """Compute the IoU of two given binary dataarrays along the given dimensions.

    We may interpret the IoU (Intersection over Union) as a similarity score
    between two sets. Considering two sets A and B, an IoU of 1 means they are
    identical, while an IoU of 0 means they are completly disjoint.
    Using dims = ("latitude", "longitude") means that we want to find the most
    similarity between spatial zones.

    For example, this is the most common use case:
    >>> lat = np.arange(10, 0, -1)
    >>> lon = np.arange(-5, 5, 1)
    >>> id0 = ['a', 'b']
    >>> id1 = ['c', 'd', 'e']
    >>> arr0 = np.array(
    ... [[[int(i > k) for i in lon] for j in lat] for k in range(len(id0))]
    ... )
    >>> arr1 = np.array(
    ... [[[int(j > 5 + k) for i in lon] for j in lat] for k in range(len(id1))]
    ... )
    >>> da0 = xr.DataArray(arr0, coords=(("id0", id0), ("lat", lat), ("lon", lon)))
    >>> da1 = xr.DataArray(arr1, coords=(("id1", id1), ("lat", lat), ("lon", lon)))
    >>> da0
    <xarray.DataArray (id0: 2, lat: 10, lon: 12)>
    array([[[...]]])
    Coordinates:
    * id0      (id0) <U1 'a' 'b'
    * lat      (lat) int64 10 9 8 7 6 5 4 3 2 1
    * lon      (lon) int64 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5
    >>> da1
    <xarray.DataArray (id1: 3, lat: 10, lon: 12)>
    array([[[...]]])
    Coordinates:
    * id1      (id1) <U1 'c' 'd' 'e'
    * lat      (lat) int64 10 9 8 7 6 5 4 3 2 1
    * lon      (lon) int64 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5
    >>> compute_iou(da0, da1, dims=("lat", "lon"))
    <xarray.DataArray (id0: 2, id1: 3)>
    array([[0.29411765, 0.25641026, 0.21126761],
        [0.25      , 0.22222222, 0.1875    ]])
    Coordinates:
    * id0      (id0) <U1 'a' 'b'
    * id1      (id1) <U1 'c' 'd' 'e'

    In this example, we created 2 binary dataarrays da0 and da1 containing
    respectively the zones ('a', 'b') and ('c', 'd', 'e'). The IoU returns us a
    table_localisation of the IoUs of all the combinations of the 2 sets of zones.

    make sure entries are of type booleans to be more efficient

    Args:
        left_da (xr.DataArray): Left dataarray
        right_da (xr.DataArray): Right DataArray
        dims (Dimension): Dimensions to apply IoU on.
            Defaults to SPACE_DIM.

    Returns:
        xr.DataArray: TableLocalisation of the computed IoU along the given dims.
    """
    if left_da.dtype != "bool":
        left_da = left_da.fillna(0).astype("int8").astype("bool")
    if right_da.dtype != "bool":
        right_da = right_da.fillna(0).astype("int8").astype("bool")
    return (left_da * right_da).sum(dims) / (right_da + left_da).sum(dims)


def _compute_iol_retained_ids(
    geos_descriptive: xr.DataArray,
    phenomenon_map: xr.DataArray,
    dims: Dimension,
    threshold_area_proportion: float,
    threshold_phenomenon_proportion: float,
) -> List[str]:
    if phenomenon_map.dtype != "bool":
        phenomenon_map = phenomenon_map.fillna(0).astype("int8").astype("bool")
    if "id" in phenomenon_map.dims:
        phenomenon_map = phenomenon_map.sum("id")
    phenomenon_size = phenomenon_map.sum()

    # we drop the zones which have a proportion of the phenomenon below the threshold
    inter = (geos_descriptive * phenomenon_map).sum(dims)
    geos_prop = inter / geos_descriptive.sum(dims)
    phenomenon_prop = inter / phenomenon_map.sum(dims)
    remaining_area = geos_descriptive[
        (geos_prop >= threshold_area_proportion)
        & (phenomenon_prop >= threshold_phenomenon_proportion)
    ]

    ids = []
    selected_prop = 0.0
    while remaining_area.count() > 0 and selected_prop < 0.9:
        map_with_exclusions = remaining_area
        if ids:
            map_with_exclusions *= geos_descriptive.sel(id=ids).sum("id") == 0
        phenomenon_map_with_exclusions = map_with_exclusions * phenomenon_map

        phenomenon_proportion = phenomenon_map_with_exclusions.sum(
            dims
        ) / map_with_exclusions.sum(dims)
        cond = phenomenon_proportion > phenomenon_proportion.max() * 0.7

        id_to_take = phenomenon_map_with_exclusions[cond].sum(dims).idxmax().item()
        ids.append(id_to_take)

        sorted_areas = geos_descriptive.sel(id=ids).sum("id") > 0
        selected_prop = (phenomenon_map * sorted_areas).sum() / phenomenon_size

        remaining_area = remaining_area.drop_sel(id=id_to_take)
        if remaining_area.count() > 0:
            inter = (remaining_area * phenomenon_map * ~sorted_areas).sum(dims)
            geos_prop = inter / remaining_area.sum(dims)
            phenomenon_prop = inter / phenomenon_map.sum(dims)

            remaining_area = remaining_area[
                (geos_prop >= threshold_area_proportion)
                & (phenomenon_prop >= threshold_phenomenon_proportion)
            ]
    return ids


def _compute_iol_clean_inclusions(
    geos_descriptive: xr.DataArray,
    phenomenon_map: xr.DataArray,
    dims: Dimension,
    ids: List[str],
    threshold_area_proportion: float,
) -> List[str]:
    if not ids:
        return []

    sorted_areas = geos_descriptive.sel(id=ids)
    sorted_areas = sorted_areas.sortby(sorted_areas.sum(dims), ascending=False)
    sorted_ids = sorted_areas.id
    i = 0
    while i < len(sorted_ids):
        ids_to_exclude = []
        for j in range(i + 1, len(sorted_ids)):
            map_with_exclusions = sorted_areas.isel(id=j) > 0
            map_size = map_with_exclusions.sum(dims)
            for k in range(i + 1):
                map_with_exclusions &= ~sorted_areas.isel(id=k) > 0

            # We exclude the nested location
            geo_prop = (map_with_exclusions & phenomenon_map).sum(dims) / map_size
            if geo_prop < threshold_area_proportion:
                ids_to_exclude.append(j)
        if ids_to_exclude:
            sorted_ids = sorted_ids.drop_isel(id=ids_to_exclude)
        i += 1
    return [id for id in ids if id in sorted_ids.id]  # to avoid unsorted values


def compute_iol(
    geos_descriptive: xr.DataArray,
    phenomenon_map: xr.DataArray,
    dims: Dimension = SPACE_DIM,
    threshold_area_proportion: float = 0.25,
    threshold_phenomenon_proportion: float = 0.1,
) -> Optional[xr.DataArray]:
    """
    Compute the IoL of two given binary dataarrays along the given dimensions.
    We may interpret the IoL (Intersection over Location) as a similarity score
    between two sets. Make sure entries are of type booleans to be more efficient

    Args:
        geos_descriptive (xr.DataArray): Containing all geos descriptive with different
                                        ids
        phenomenon_map (xr.DataArray): Map of the phenomenon
        dims (Dimension): Dimensions to apply IoL on.
            Defaults to SPACE_DIM.
        threshold_area_proportion (float): Minimal proportion of the phenomenon in an
            area over the size of area
        threshold_phenomenon_proportion (float): Minimal proportion of the phenomenon in
            an area over the size of phenomenon

    Returns:
        xr.DataArray: TableLocalisation of the computed IoL along the given dims.
    """
    if geos_descriptive.dtype != "bool":
        geos_descriptive = geos_descriptive.fillna(0).astype("int8").astype("bool")

    ids = _compute_iol_retained_ids(
        geos_descriptive,
        phenomenon_map,
        dims,
        threshold_area_proportion,
        threshold_phenomenon_proportion,
    )

    # we delete subareas contained in a selected area
    ids = _compute_iol_clean_inclusions(
        geos_descriptive, phenomenon_map, dims, ids, threshold_area_proportion
    )

    return geos_descriptive.sel(id=ids) if len(ids) > 0 else None


def compute_iol_left(
    left_da: xr.DataArray, right_da: xr.DataArray, dims: Dimension = SPACE_DIM
) -> xr.DataArray:
    """Compute the IoL of two given binary dataarrays along the given dimensions.

    Args:
        left_da (xr.DataArray): Left dataarray
        right_da (xr.DataArray): Right DataArray
        dims (Dimension): Dimensions to apply IoU on.
            Defaults to SPACE_DIM.

    Returns:
        xr.DataArray: TableLocalisation of the computed IoL along the given dims.
    """
    if left_da.dtype != "bool":
        left_da = left_da.fillna(0).astype("int8").astype("bool")
    if right_da.dtype != "bool":
        right_da = right_da.fillna(0).astype("int8").astype("bool")
    return (left_da * right_da).sum(dims) / (1.0 * left_da.sum(dims))


def generic_merge(
    left_da: Optional[xr.DataArray], right_da: Optional[xr.DataArray]
) -> xr.DataArray:
    """
    Merges two DataArrays, handling situations where one or both DataArrays might be
    None.

    This function performs a safe merge of two DataArrays. If either `left_da` or
    `right_da` is None, it returns the non-None DataArray. Otherwise, it uses
    `xr.merge` to combine the DataArrays and returns the merged DataArray with the
    name matching the original left DataArray's name.

    Args:
        left_da (Optional[xr.DataArray]): The first DataArray to merge.
        right_da (Optional[xr.DataArray]): The second DataArray to merge.

    Returns:
        xr.DataArray: The merged DataArray, or the non-None DataArray if one is None.
    """
    if left_da is None:
        return right_da
    if right_da is None:
        return left_da
    return xr.merge([left_da, right_da])[left_da.name]


class GenericArea:
    """
    Class to contain and manipulate combinations of areas.

    Args:
        mask_da (Optional[xr.DataArray]): DataArray containing the mask applied for
            prior risk calculations. Defaults to None.
        alt_min (Optional[int]): Altitude min boundary. Defaults to ALT_MIN.
        alt_max (Optional[int]): Altitude max boundary. Defaults to ALT_MAX.
        spatial_dims (Dimension): Spatial dimensions to apply aggregation
            functions to. Defaults to SPACE_DIM.
    """

    def __init__(
        self,
        mask_da: Optional[xr.DataArray] = None,
        alt_min: Optional[int] = ALT_MIN,
        alt_max: Optional[int] = ALT_MAX,
        spatial_dims: Dimension = SPACE_DIM,
    ):
        """
        Create a generic area object.

        Args:
            mask_da: The mask DataArray.
            alt_min: The minimum altitude.
            alt_max: The maximum altitude.
            spatial_dims: The spatial dimensions.

        """
        self.mask_da: Optional[xr.DataArray] = mask_da
        self.alt_min: int = int(alt_min) if alt_min is not None else ALT_MIN
        self.alt_max: int = int(alt_max) if alt_max is not None else ALT_MAX
        self.spatial_dims: Union[str, Sequence[str]] = (
            spatial_dims if spatial_dims is not None else SPACE_DIM
        )

    @property
    def alt_kwargs(self) -> Dict[str, int]:
        """Property to provide alt_min and alt_max as a mapping to use as keyword
        arguments.
        """
        return {"alt_min": self.alt_min, "alt_max": self.alt_max}

    def filter_areas(
        self, area_da: xr.DataArray, areas_list_da: xr.DataArray
    ) -> List[str]:
        """
        This function filters all areas that completely include or are completely
        disjoint from the area being divided. These areas are not interesting.

        Args:
            area_da (dataArray): The area being divided.
            areas_list_da (xr.DataArray): DataArray containing a list of valid areas.
        returns:
            List[str] : List of the ids of the areas "included" in the area.
        """
        squeezed_da = area_da.squeeze()
        product = (areas_list_da * squeezed_da).sum(self.spatial_dims)
        idx = (product >= 1) & (product < squeezed_da.sum(self.spatial_dims))
        return areas_list_da.where(idx, drop=True).id.values.tolist()

    def rename_inter(
        self, domain_name: str, area_name: Union[str, List[str]]
    ) -> Union[str, List[str]]:
        """Rename the area that is the intersection between a given domain_name
        and a sub_area_name.

        !Warning: We suppose that the sub_area is included in the domain. The goal of
        that method is to provide the corresponding name of such an intersection.

        For instances:
        >> gen = GenericArea(..., alt_min=500, alt_max=2000)
        >> gen.rename_inter('en Isère', ['à Grenoble', 'entre 1000 m et 1500 m',
        ..     'entre 1000 m et 2000 m']
        .. )
        ['à Grenoble', 'entre 1000 m et 1500 m', 'au-dessus de 1000 m']
        >> gen.rename_inter('au-dessus de 1500 m', 'sur le massif de Belledonne')
        'sur le massif de Belledonne au-dessus de 1500 m'
        >> gen.rename_inter('entre 1500 m et 2000 m', 'sur le massif de Belledonne')
        'sur le massif de Belledonne au-dessus de 1500 m'
        >> gen.rename_inter('entre 1000 m et 1800 m', 'au-dessus de 1500 m')
        'entre 1500 m et 1800 m'
        >> gen.rename_inter('entre 1000 m et 2000 m', 'au-dessus de 1500 m')
        'au-dessus de 1500 m'

        Args:
            domain_name (str): Name of the area considered as the domain.
                The concept of domain is important here because we will not rephrase the
                domain's name if not necessary (contrary to the sub_area).
            area_name (Union[str, List[str]]): Name of the area(s) we will intersect
                with the domain.

        Returns:
            Union[str, List[str]]: Name(s) of the intersection between the area(s)
            and the domain.
        """
        if isinstance(area_name, List):
            return [self.rename_inter(domain_name, sub_area) for sub_area in area_name]

        domain_interval = AltitudeInterval.from_str(domain_name)
        sub_area_interval = AltitudeInterval.from_str(area_name)
        if bool(domain_interval):
            if bool(sub_area_interval):
                return (domain_interval & sub_area_interval).name(**self.alt_kwargs)
            return f"{area_name} {domain_interval.name(**self.alt_kwargs)}"
        if bool(sub_area_interval):
            return sub_area_interval.name(**self.alt_kwargs)
        return area_name

    def rename_difference(
        self, domain_name: str, area_name: Union[str, List[str]]
    ) -> Union[str, List[str]]:
        """Rename the area that is the difference between a given domain_name
        and area names.

        !Warning: We suppose that the sub_area is included in the domain. The goal of
        that method is to provide the corresponding name of such a difference.

        For instances:
        >>> gen = GenericArea(..., alt_min=500, alt_max=2000)
        >>> gen.rename_difference('en Isère', ['à Grenoble', 'entre 1000 m et 1500',
        ...     'entre 1000 m et 2000 m']
        ... )
        ['comp_à Grenoble', 'en dessous de 1000 m et au-dessus de 1500 m', 'en dessous
            de 1000 m']
        >>> gen.rename_difference(
        ...     'au-dessus de 1500 m', 'sur le massif de Belledonne'
        ... )
        'au-dessus de 1500 m sauf sur le massif de Belledonne']
        >>> gen.rename_difference(
        ...     'entre 1500 m et 2000 m', 'sur le massif de Belledonne',
        ... )
        'au-dessus de 1500 m sauf sur le massif de Belledonne'
        >>> gen.rename_difference(
        ...    'entre 1000 m et 1800 m', 'au-dessus de 1500 m'
        ... )
        'entre 1000 m et 1500 m'
        >>> gen.rename_difference(
        ...    'entre 500 m et 1800 m', 'au-dessus de 1500 m'
        ... )
        'en dessous de 1500 m'

        Args:
            domain_name (str): Name of the area considered as the domain.
                The concept of domain is important here because we will not rephrase the
                domain's name if not necessary (contrary to the sub_area).
            area_name (Union[str, List[str]]): Name of the area(s) we will intersect
                with the domain.

        Returns:
            Union[str,Iterable[str]]: Name(s) of the difference between the area(s)
            and the domain.
        """
        if isinstance(area_name, List):
            return [
                self.rename_difference(domain_name, sub_area) for sub_area in area_name
            ]

        domain_interval = AltitudeInterval.from_str(domain_name)
        sub_area_interval = AltitudeInterval.from_str(area_name)
        if bool(domain_interval):
            if bool(sub_area_interval):
                return domain_interval.difference(sub_area_interval).name(
                    **self.alt_kwargs
                )
            return f"{domain_interval.name(**self.alt_kwargs)} {_('sauf')} {area_name}"
        if bool(sub_area_interval):
            return f"{(~sub_area_interval).name(**self.alt_kwargs)}"
        return f"comp_{area_name}"
