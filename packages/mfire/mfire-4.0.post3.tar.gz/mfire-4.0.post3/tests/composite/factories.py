import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, cast

import numpy as np

import mfire.utils.mfxarray as xr
from mfire.composite.aggregation import Aggregation, AggregationMethod, AggregationType
from mfire.composite.base import BaseComposite
from mfire.composite.component import (
    RiskComponentComposite,
    SynthesisComponentComposite,
    SynthesisComposite,
    SynthesisCompositeInterface,
)
from mfire.composite.event import (
    Category,
    EventAccumulationComposite,
    EventComposite,
    Threshold,
)
from mfire.composite.field import FieldComposite, Selection
from mfire.composite.geo import AltitudeComposite, GeoComposite
from mfire.composite.level import LevelComposite, LocalisationConfig
from mfire.composite.operator import ComparisonOperator, LogicalOperator
from mfire.composite.period import PeriodComposite, PeriodsComposite
from mfire.composite.production import ProductionComposite
from mfire.composite.serialized_types import s_datetime, s_path, s_slice
from mfire.settings import SETTINGS_DIR
from mfire.utils.date import Datetime
from mfire.utils.string import _
from tests.factories import Factory
from tests.utils.factories import PeriodDescriberFactory


class PeriodCompositeFactory(PeriodComposite):
    id: str = "period_id"
    name: Optional[str] = "period_name"
    start: s_datetime = Datetime(2023, 3, 1)
    stop: s_datetime = Datetime(2023, 3, 5)


class PeriodsCompositeFactory(PeriodsComposite):
    periods: List[PeriodComposite] = [PeriodCompositeFactory()]


class AggregationFactory(Aggregation):
    method: AggregationMethod = AggregationMethod.MEAN
    kwargs: dict = {}


class SelectionFactory(Selection):
    sel: dict = {"id": random.randint(0, 42)}
    islice: dict[str, s_slice | float] = {
        "valid_time": slice(random.randint(0, 42), random.randint(0, 42))
    }
    isel: dict = {"latitude": random.randint(0, 42)}
    slice: dict[str, s_slice] = {
        "longitude": slice(random.randint(0, 42), random.randint(0, 42))
    }


class BaseCompositeFactory(Factory, BaseComposite):
    pass


class ProductionCompositeFactory(BaseCompositeFactory, ProductionComposite):
    id: str = "production_id"
    name: str = "production_name"
    config_hash: str = "production_config_hash"
    mask_hash: str = "production_mask_hash"
    sort: float = 1.1
    components: List[Union[RiskComponentComposite, SynthesisComponentComposite]] = []


class FieldCompositeFactory(BaseCompositeFactory, FieldComposite):
    """Field composite factory class."""

    file: Union[Path, List[Path]] = Path("field_composite_path")
    grid_name: str = "franxl1s100"
    name: str = "field_name"


class GeoCompositeFactory(BaseCompositeFactory, GeoComposite):
    """Geo composite factory class."""

    file: s_path = Path("geo_composite_file")
    mask_id: Optional[Union[List[str], str]] = "mask_id"
    grid_name: Optional[str] = "franxl1s100"


class AltitudeCompositeFactory(BaseCompositeFactory, AltitudeComposite):
    """Altitude composite factory class."""

    filename: s_path = Path(SETTINGS_DIR / "geos/altitudes/franxl1s100.nc")
    grid_name: str = "franxl1s100"
    name: str = "name"


class EventCompositeFactory(BaseCompositeFactory, EventComposite):
    """Factory class for creating EventComposite objects."""

    field: FieldComposite = FieldCompositeFactory()
    category: Category = Category.BOOLEAN
    altitude: AltitudeComposite = AltitudeCompositeFactory()
    geos: Union[GeoComposite, xr.DataArray] = GeoCompositeFactory()
    plain: Optional[Threshold] = Threshold(
        threshold=20, comparison_op=ComparisonOperator.SUPEGAL, units="mm"
    )
    aggregation: Optional[Aggregation] = AggregationFactory()


class EventAccumulationCompositeFactory(
    EventCompositeFactory, EventAccumulationComposite
):
    """Factory class for creating EventAccumulationComposite objects."""

    field_1: FieldComposite = FieldCompositeFactory()
    cum_period: int = 6


class LevelCompositeFactory(BaseCompositeFactory, LevelComposite):
    level: int = 2
    aggregation: Optional[Aggregation] = None
    aggregation_type: AggregationType = AggregationType.UP_STREAM
    events: List[Union[EventAccumulationComposite, EventComposite]] = [
        EventCompositeFactory()
    ]
    localisation: LocalisationConfig = LocalisationConfig()

    def __init__(self, **data: Any):
        events = data.get("events")
        if events is not None and data.get("logical_op_list") is None:
            logical_ops = [op.value for op in LogicalOperator]
            data["logical_op_list"] = list(
                np.random.choice(logical_ops, size=len(events) - 1)
            )
        super().__init__(**data)


class SynthesisComponentCompositeFactory(
    BaseCompositeFactory, SynthesisComponentComposite
):
    period: PeriodComposite = PeriodCompositeFactory()
    id: str = "text_component_id"
    name: str = "text_component_name"
    production_id: str = "production_id"
    production_name: str = "production_name"
    production_datetime: s_datetime = Datetime(2023, 3, 1, 6)

    weathers: List[SynthesisComposite] = []
    product_comment: bool = True

    customer_id: Optional[str] = "customer_id"
    customer_name: Optional[str] = "customer_name"


class RiskComponentCompositeFactory(BaseCompositeFactory, RiskComponentComposite):
    period: PeriodComposite = PeriodCompositeFactory()
    id: str = "risk_component_id"
    name: str = "risk_component_name"
    production_id: str = "production_id"
    production_name: str = "production_name"
    production_datetime: s_datetime = Datetime(2023, 3, 1, 6)

    levels: List[LevelComposite] = []
    hazard_id: str = "hazard_id"
    hazard_name: str = "hazard_name"
    product_comment: bool = True
    params: Dict[str, FieldComposite] = {}

    customer_id: Optional[str] = "customer_id"
    customer_name: Optional[str] = "customer_name"


class SynthesisCompositeInterfaceFactory(SynthesisCompositeInterface):
    has_risk: Any = lambda x, y, z: None
    has_field: Any = lambda x, y, z: None


class SynthesisCompositeFactory(BaseCompositeFactory, SynthesisComposite):
    id: str = "id_weather"
    params: Dict[str, FieldComposite] = {}
    units: Dict[str, Optional[str]] = {}
    localisation: LocalisationConfig = LocalisationConfig()

    interface: SynthesisCompositeInterface = SynthesisCompositeInterfaceFactory()
    component: Optional[
        SynthesisComponentComposite
    ] = SynthesisComponentCompositeFactory(
        period_describer_factory=PeriodDescriberFactory()
    )

    @classmethod
    def create_factory(
        cls,
        geos_descriptive: list,
        valid_times: list,
        lon: list,
        lat: list,
        data_vars: dict,
        altitude: Optional[list],
        **kwargs,
    ) -> SynthesisComposite:
        data_ds = xr.Dataset(
            data_vars=data_vars,
            coords={
                "id": "id_axis",
                "valid_time": valid_times,
                "latitude": lat,
                "longitude": lon,
            },
        )

        ids = list(map(str, list(range(len(geos_descriptive)))))
        geos_descriptive = xr.DataArray(
            data=geos_descriptive,
            dims=["id", "latitude", "longitude"],
            coords={
                "id": ids,
                "latitude": lat,
                "longitude": lon,
                "areaType": (["id"], ["Axis"] + (len(ids) - 1) * [""]),
                "areaName": (
                    ["id"],
                    [f"à localisation N°{i + 1}" for i in range(len(ids))],
                ),
            },
        )
        compo = cls(
            compute_factory=lambda **_kwargs: data_ds,
            production_datetime=data_ds.valid_time[0],
            geos_descriptive_factory=lambda _: geos_descriptive,
            altitude_factory=lambda _: xr.DataArray(
                data=altitude,
                dims=["latitude", "longitude"],
                coords={"latitude": lat, "longitude": lon},
            ),
            **kwargs,
        )

        geos_data = geos_descriptive.sum(dim="id").expand_dims({"id": ["id_axis"]}) > 0
        geos_data["areaType"] = (["id"], ["Axis"])
        geos_data["areaName"] = (["id"], [_("sur tout le domaine")])
        geos_data["altAreaName"] = (["id"], [_("sur tout le domaine")])
        compo.geos = GeoCompositeFactory(
            compute_factory=lambda: geos_data, mask_da_factory=geos_data, mask_id=None
        )
        return cast(SynthesisComposite, compo)
