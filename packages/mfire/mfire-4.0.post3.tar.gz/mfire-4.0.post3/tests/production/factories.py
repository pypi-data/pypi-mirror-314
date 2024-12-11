from __future__ import annotations

from typing import List, Optional

from mfire.composite.serialized_types import s_datetime
from mfire.production.base import BaseCDPComponent
from mfire.production.component import CDPComponents, CDPRisk, CDPText
from mfire.production.dataset import CDPDataset, CDPSummary, CDPValueParam
from mfire.production.period import CDPPeriod
from mfire.production.production import CDPProduction
from mfire.utils.date import Datetime


class CDPSummaryFactory(CDPSummary):
    ValidityDate: Optional[s_datetime] = Datetime(2023, 3, 1)
    Level: int = 1
    Values: List[CDPValueParam] = []


class CDPDatasetFactory(CDPDataset):
    ShortSummary: CDPSummary = CDPSummaryFactory()
    Summary: List[CDPSummary] = [CDPSummaryFactory()]


class CDPPeriodFactory(CDPPeriod):
    PeriodId: str = "period_id"
    PeriodName: str = "period_name"
    DateDebutPeriode: s_datetime = Datetime(2023, 3, 1)
    DateFinPeriode: s_datetime = Datetime(2023, 3, 3)


class BaseCDPComponentFactory(BaseCDPComponent):
    ComponentId: str = "component_id"
    ComponentName: str = "component_name"
    Period: CDPPeriod = CDPPeriodFactory()
    GeoId: str = "geo_id"
    GeoName: str = "geo_name"


class CDPRiskFactory(BaseCDPComponentFactory, CDPRisk):
    HazardId: str = "hazard_id"
    HazardName: str = "hazard_name"
    Dataset: CDPDataset = CDPDatasetFactory()
    DetailComment: str = "detail_comment"


class CDPTextFactory(BaseCDPComponentFactory, CDPText):
    SyntText: str = "synt_text"


class CDPComponentsFactory(CDPComponents):
    Aleas: Optional[List[CDPRisk]] = [CDPRiskFactory()]
    Text: Optional[List[CDPText]] = [CDPTextFactory()]


class CDPProductionFactory(CDPProduction):
    ProductionId: str = "production_id"
    ProductionName: str = "production_name"
    CustomerId: Optional[str] = "customer_id"
    CustomerName: Optional[str] = "customer_name"
    DateBulletin: s_datetime = Datetime(2023, 3, 1, 7)
    DateProduction: s_datetime = Datetime(2023, 3, 1, 6)
    DateConfiguration: s_datetime = Datetime(2023, 2, 1)
    Components: CDPComponents = CDPComponentsFactory()
