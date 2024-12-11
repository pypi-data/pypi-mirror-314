from __future__ import annotations

import operator
from enum import Enum
from pathlib import Path
from typing import ClassVar, Dict, List, Optional, Tuple, Union

from pydantic import model_validator

from mfire.composite.base import BaseModel
from mfire.composite.geo import GeoComposite
from mfire.utils import mfxarray as xr
from mfire.utils.xr import MaskLoader, da_set_up


class AggregationType(str, Enum):
    """Création d'une classe d'énumération contenant les differents
    types d'aggregation
    """

    UP_STREAM = "upStream"
    DOWN_STREAM = "downStream"


class AggregationMethod(str, Enum):
    """
    Enumeration of aggregation methods.

    Args:
        value (str): String value of the Aggregation Method
        is_post_aggregation (bool): Indicates whether a method must be applied after
            data aggregation.

            This flag determines if a particular method can only be used on aggregated
            data. Some methods, like calculating density, require combining individual
            values before comparison with a threshold. Other methods, like finding the
            mean, can be applied directly to individual values.

            Examples:
                * 'density': True (requires aggregation before use)
                * 'mean': False (can be used directly on individual values)

    Returns:
        AggregationMethod: New AggregationMethod object
    """

    MEAN = ("mean", False)
    DENSITY = ("density", True)
    RDENSITY = ("requiredDensity", True)
    RDENSITY_WEIGHTED = ("requiredDensityWeighted", True)
    RDENSITY_CONDITIONAL = ("requiredDensityConditional", True)
    ALL = ("all", True)
    ANY = ("any", True)
    MAX = ("max", False)
    MIN = ("min", False)
    MEDIAN = ("median", False)
    SUM = ("sum", False)
    STD = ("std", False)
    VAR = ("var", False)
    QUANTILE = ("quantile", False)

    def __new__(cls, value: str, is_post_aggregation: bool) -> AggregationMethod:
        """
        Initialize a new AggregationMethod object.

        Args:
            value (str): String value of the Aggregation Method
            is_post_aggregation (bool): Whether the given method is to use
                only after aggregation. For instance, given a field of floating values:
                * 'density' method is is_post_aggregation because the expression
                    "density(field) > threshold" has no sense.
                * 'mean' method is not is_post_aggregation because the expression
                    "mean(field) > threshold" has a sense.

        Returns:
            AggregationMethod: New AggregationMethod object
        """
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._is_post_aggregation = is_post_aggregation
        return obj

    def __str__(self) -> str:
        """
        Return a string representation of the AggregationMethod object.

        Returns:
            str: String representation of the AggregationMethod object
        """
        return self._value_

    @property
    def is_post_aggregation(self) -> bool:
        """
        Return whether the AggregationMethod object is to be used only after
        aggregation.

        Returns:
            bool: True if the AggregationMethod object is to be used only after
            aggregation, False otherwise
        """
        return self._is_post_aggregation


class Aggregation(BaseModel):
    """Configuration object for aggregation methods in the Promethee production task.

    Args:
        baseModel (model): The model from the pydantic library.

    Returns:
        baseModel: Aggregation object.
    """

    method: AggregationMethod
    kwargs: Dict = {}

    DEFAULT_ARGUMENTS: ClassVar[dict] = {
        "density": {},
        "requiredDensity": {"dr": 0.5},
        "requiredDensityWeighted": {
            "dr": 0.5,  # Le threshold par defaut
            "central_weight": 10,  # la ponderation dans la zone
            "outer_weight": 1,  # La ponderation en dehors de la zone
        },
        "requiredDensityConditional": {"dr": 0.5},
        "all": {},
        "any": {},
        "max": {},
        "mean": {},
        "median": {},
        "min": {},
        "sum": {},
        "std": {},
        "var": {},
        "quantile": {"q": 0.5},
    }

    @model_validator(mode="after")
    def check_method_kwargs(self) -> Aggregation:
        """Validate the method's kwargs based on the aggregation method.

        Returns:
            AggregationMethod: The validated aggregation method.

        Raises:
            ValueError: If kwargs do not match the aggregation method.
        """

        dic_kwargs = self.DEFAULT_ARGUMENTS[self.method].copy()
        dic_kwargs.update({k: v for k, v in self.kwargs.items() if v is not None})

        # Define the missing and unexpected keys based on the aggregation method
        missing_keys = {
            AggregationMethod.RDENSITY_CONDITIONAL: ["central_mask"],
            AggregationMethod.RDENSITY_WEIGHTED: ["central_mask"],
        }
        unexpected_keys = {
            AggregationMethod.MEAN: [
                "dr",
                "central_weight",
                "outer_weight",
                "central_mask",
            ],
            AggregationMethod.RDENSITY: [
                "central_weight",
                "outer_weight",
                "central_mask",
            ],
            AggregationMethod.RDENSITY_CONDITIONAL: ["central_weight", "outer_weight"],
        }

        missing = [
            key
            for key in missing_keys.get(self.method, {})
            if dic_kwargs.get(key) is None
        ]
        if missing:
            raise ValueError(f"Missing expected values: {missing}")

        unexpected = [
            key
            for key in unexpected_keys.get(self.method, {})
            if dic_kwargs.get(key) is not None
        ]
        if unexpected:
            raise ValueError(f"Unexpected values: {unexpected}")

        self.kwargs = dic_kwargs

        return self

    @staticmethod
    def from_configuration(
        aggregation: Optional[dict], mask_file: Path, grid_name: Optional[str] = None
    ) -> Optional[Aggregation]:
        """
        Creates an Aggregation object from a configuration dictionary and mask file
        path.

        Args:
            aggregation (Optional[Dict]): A dictionary containing the aggregation
                configuration. If None, None is returned.
            mask_file (Path): The path to the mask file used for aggregation.
            grid_name (Optional[str]): The optional grid name to use for GeoComposite
                creation.

        Returns:
            Optional[Aggregation]: An Aggregation object based on the configuration, or
                None if the configuration is missing.
        """

        if aggregation is None:
            return None

        # Extract kwargs dictionary from the aggregation config (or use an empty one)
        kwargs = aggregation.get("kwargs", {})
        new_kwargs = {}

        # Handle "dr" parameter (supporting various keys with conditional logic)
        if "dr" in kwargs:
            new_kwargs["dr"] = kwargs["dr"]
        elif "drConditional" in kwargs:
            new_kwargs["dr"] = kwargs["drConditional"]
        elif "drCentralZone" in kwargs:
            new_kwargs["dr"] = kwargs["drCentralZone"]

        # Ensure "dr" is a float within the valid range (0.01 - 1.0)
        if "dr" in new_kwargs:
            new_kwargs["dr"] = float(new_kwargs["dr"])
            if 1 < new_kwargs["dr"] <= 100:
                new_kwargs["dr"] = new_kwargs["dr"] / 100.0

        # Extract optional parameters ("central_weight" and "outer_weight")
        if central_weight := kwargs.get("centralWeight"):
            new_kwargs["central_weight"] = central_weight
        if outer_weight := kwargs.get("outerWeight"):
            new_kwargs["outer_weight"] = outer_weight

        # Handle "central_mask" parameter (supporting different key names)
        for central_key in ("centralZone", "centralZoneConditional"):
            if central_zone := kwargs.get(central_key):
                new_kwargs["central_mask"] = GeoComposite(
                    file=mask_file, mask_id=central_zone, grid_name=grid_name
                )
                break

        # Create the Aggregation object using the method and new kwargs
        return Aggregation(method=aggregation["method"], kwargs=new_kwargs)

    @property
    def is_post(self) -> bool:
        return self.method.is_post_aggregation

    @property
    def is_pre(self) -> bool:
        return not self.method.is_post_aggregation


class InputError(ValueError):
    pass


class Aggregator:
    """
    Class for aggregating fields (xr.DataArray)
    """

    def __init__(
        self, da: xr.DataArray, aggregate_dim: Optional[Union[List[str], str]] = None
    ):
        """
        Initialize an Aggregator object.

        Args:
            da (xarray.DataArray) - Fields to be aggregated
            mask (xarray.DataArray, optional) - Mask to apply
            aggregate_dim (str or sequence of str, optional) - Dimension(s) over
                which to apply aggregation.

        """
        self.da = da.copy(deep=True)

        if aggregate_dim is None:
            self.aggregate_dim = ["latitude", "longitude"]
        else:
            self.aggregate_dim = aggregate_dim

    def compute(self, aggregation: Aggregation) -> xr.DataArray:
        """
        Aggregates self.da DataArray using the specific 'method' over
        the self.aggregate_dim dimension(s)

        Args:
            aggregation (Aggregation) - Aggregation method

        Returns:
            reduced (xarray.DataArray) - New DataArray object with the
                method applied to its data and the self.aggregate_dim removed.

        """
        # Apply the aggregation method
        if aggregation.method == AggregationMethod.DENSITY:
            return self.density(**aggregation.kwargs)
        if aggregation.method == AggregationMethod.RDENSITY:
            return self.required_density(**aggregation.kwargs)
        if aggregation.method == AggregationMethod.RDENSITY_WEIGHTED:
            return self.drr_weighted(**aggregation.kwargs)
        if aggregation.method == AggregationMethod.RDENSITY_CONDITIONAL:
            return self.drr_conditional(**aggregation.kwargs)
        return getattr(self.da, aggregation.method)(
            dim=self.aggregate_dim, **aggregation.kwargs
        )

    def density(self, **kwargs) -> xr.DataArray:
        """
        Returns the density risk (Densité De Risque) of the self.da DataArray
        over the self.aggregate_dim dimension(s)

        Args:
            **kwargs (dict) - Keyword arguments specific to xarray's sum method.

        Returns:
            reduced (xarray.DataArray) - New DataArray object with the ddr
                applied to its data and the self.aggregate_dim removed.

        """
        return self.da.sum(dim=self.aggregate_dim, **kwargs) / self.da.count(
            dim=self.aggregate_dim, **kwargs
        )

    def required_density(self, dr: float, **kwargs) -> xr.DataArray:
        """
        Apply a threshold to the density risk of the self.da DataArray
                over the self.aggregate_dim dimension(s).

        Args:
            dr (float in range [0, 1]): Threshold to apply.
            **kwargs (dict): Keyword arguments specific to the previous
                ddr method.

        Returns:
            reduced (xarray.DataArray): New DataArray object with 'thresholded ddr'
            applied to its data and the self.aggregate_dim removed.
        """
        # Check that the threshold is in the valid range.
        if dr > 1 or dr < 0:
            raise InputError(f"Threshold given = {dr}, while expected to be in [0,1].")

        # Apply the threshold to the density risk.
        thresholded_ddr = self.density(**kwargs) > dr

        # Return a new DataArray with the thresholded density risk.
        return thresholded_ddr

    def _get_central_mask(
        self, central_mask: dict
    ) -> Tuple[xr.DataArray, xr.DataArray]:
        """
        Load the mask, crop it, and put it on the correct grid so that
            calculations are fast.

        Args:
            central_mask (dict): Contains file and mask_id.
        """

        # Open the dataset containing the mask.
        mask = (
            MaskLoader(
                filename=central_mask["file"],
                grid_name=self.da.attrs["PROMETHEE_z_ref"],
            )
            .load(ids=central_mask["mask_id"])
            .isel(id=0)
        )

        # Set up the mask for use with the DataArray.
        central_mask = da_set_up(mask, self.da)

        # Extract a central mask and a peripheral mask.
        return central_mask, mask - central_mask

    def drr_conditional(self, dr: float, central_mask: dict, **kwargs) -> xr.DataArray:
        """
        Calculates the risk occurrence, taking into account that if a pixel
        in the central area is affected, then the risk is raised.

        Args:
            thresh (float): An integer between 0 and 1 telling us what the
                density to reach is
            central_mask (dict): Dictionary containing the path and the id of the
                mask

        Returns:
            [data_array]: The risk occurrence
        """
        if dr > 1 or dr < 0:
            raise InputError(f"Threshold given = {dr}, while expected to be in [0,1].")

        central_mask, _ = self._get_central_mask(central_mask)

        # Calculate the risk based on the density
        risk_1 = self.density(**kwargs) > dr

        # Calculate the risk in the risk area
        risk_2 = (self.da * central_mask).sum(dim=self.aggregate_dim) > 0

        # If the risk depending on the density is activated or if the risk talking
        # about the central area is activated.
        return operator.or_(risk_1, risk_2)

    def drr_weighted(
        self, dr, central_mask, central_weight, outer_weight
    ) -> xr.DataArray:
        """
        Calculates the risk occurrence, taking into account a weighted density
        (between central area and outer area)

        Args:
            thresh (float): An integer between 0 and 1 telling us what the density to
                reach is
            central_mask (dict): Dictionary containing the path and the id of the
                mask
            central_weight (int): Weight inside the central area
            outer_weight (int): Weight outside the central area

        Returns:
            [data_array]: The risk occurrence
        """
        if dr > 1 or dr < 0:
            raise InputError(f"Threshold given = {dr}, while expected to be in [0,1].")

        central_mask, periph_mask = self._get_central_mask(central_mask)
        central_pix = central_mask.sum(dim=self.aggregate_dim).values
        out_pix = periph_mask.sum(dim=self.aggregate_dim).values
        total_pix = central_weight * central_pix + outer_weight * out_pix
        density = (
            (self.da * periph_mask).sum(dim=self.aggregate_dim) * outer_weight
            + (self.da * central_mask).sum(dim=self.aggregate_dim) * central_weight
        ) / total_pix
        return density > dr
