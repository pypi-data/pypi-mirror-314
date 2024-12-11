from mfire.composite.component import RiskComponentComposite
from mfire.localisation.risk_localisation import RiskLocalisation
from mfire.localisation.spatial_localisation import SpatialLocalisation
from mfire.localisation.table_localisation import TableLocalisation
from mfire.utils import mfxarray as xr
from mfire.utils.date import Datetime
from tests.composite.factories import RiskComponentCompositeFactory
from tests.factories import Factory
from tests.utils.factories import PeriodDescriberFactory


class SpatialLocalisationFactory(Factory, SpatialLocalisation):
    risk_component: RiskComponentComposite = RiskComponentCompositeFactory(
        period_describer_factory=PeriodDescriberFactory()
    )
    geo_id: str = "geo_id"


class TableLocalisationFactory(Factory, TableLocalisation):
    data: xr.DataArray = xr.DataArray(coords={"id": []}, dims=["id"])
    spatial_localisation: SpatialLocalisation = SpatialLocalisationFactory()

    alt_min: int = 100
    alt_max: int = 1000


class RiskLocalisationFactory(Factory, RiskLocalisation):
    risk_component: RiskComponentCompositeFactory = RiskComponentCompositeFactory()
    risk_level: int = 2
    geo_id: str = "geo_id"
    period: set = {Datetime(2023, 3, 1, 6)}
