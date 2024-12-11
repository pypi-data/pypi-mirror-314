from typing import Optional, Union
from zoneinfo import ZoneInfo

from mfire.composite.base import BaseModel
from mfire.composite.component import (
    RiskComponentComposite,
    SynthesisComponentComposite,
)
from mfire.settings import get_logger
from mfire.text.risk.builder import RiskBuilder
from mfire.text.synthesis.temperature import TemperatureBuilder
from mfire.text.synthesis.weather import WeatherBuilder
from mfire.text.synthesis.wind import WindBuilder
from mfire.utils.string import _

LOGGER = get_logger(name="text_manager.mod", bind="text_manager")


class Manager(BaseModel):
    """
    Class for dispatching the text generation according to the given risk_component's
    type.

    Args:
        component: The text risk_component to handle.
    """

    component: Union[RiskComponentComposite, SynthesisComponentComposite]

    builders: dict = {
        "risk": RiskBuilder,
        "tempe": TemperatureBuilder,
        "weather": WeatherBuilder,
        "wind": WindBuilder,
    }

    def _compute_text(self, geo_id: str) -> str:
        """
        Compute in the case of text (synthesis or, maybe one day, sitgen)

        Returns:
            str: The computed text.
        """
        return self._compute_synthesis(geo_id=geo_id)

    def _compute_synthesis(self, geo_id: str) -> str:
        """
        Compute in the case of text synthesis

        Returns:
            str: The computed text synthesis.
        """
        # Add the text title with the date
        # Currently we only use the Paris Timezone - see #36169
        zone_info = ZoneInfo("Europe/Paris")
        start = max(
            self.component.period.start, self.component.production_datetime
        ).astimezone(zone_info)
        stop = self.component.period.stop.astimezone(zone_info)

        text = _(
            "De {start_date} à {start_hour}h jusqu'au {stop_date} à {stop_hour}h :\n"
        ).format(
            start_date=f"{start.weekday_name} {start.strftime('%d')}",
            start_hour=start.strftime("%H"),
            stop_date=f"{stop.weekday_name} {stop.strftime('%d')}",
            stop_hour=stop.strftime("%H"),
        )

        has_checked_one_condition = False
        for weather_composite in self.component.weathers:
            computed_text = self.builders[weather_composite.id](
                geo_id=geo_id, composite=weather_composite
            ).compute()
            if computed_text is not None:
                text += computed_text + "\n"
                has_checked_one_condition = True
        if not has_checked_one_condition:
            text += _("RAS")

        return text

    def _compute_risk(self, geo_id: Optional[str]) -> str:
        """
        Compute in the case of risk text

        Returns:
            str: The computed risk text.
        """
        return self.builders["risk"](composite=self.component, geo_id=geo_id).compute()

    def compute(self, geo_id: str) -> str:
        """Produce a text according to the given risk_component type.

        Args:
            geo_id (str, optional): Optional geo_id for comment generation.
                Defaults to None.

        Returns:
            str: Text corresponding to the risk_component and the given geo_id.
        """
        return (
            self._compute_text(geo_id=geo_id)
            if isinstance(self.component, SynthesisComponentComposite)
            else (self._compute_risk(geo_id=geo_id))
        )
