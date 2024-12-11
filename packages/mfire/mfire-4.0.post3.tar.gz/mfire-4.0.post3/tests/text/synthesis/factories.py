from typing import Optional

from mfire.composite.component import SynthesisComposite
from mfire.text.synthesis.reducer import SynthesisReducer
from mfire.text.synthesis.temperature import TemperatureBuilder
from mfire.text.synthesis.weather import WeatherBuilder, WeatherReducer
from tests.composite.factories import SynthesisCompositeFactory
from tests.text.base.factories import BaseBuilderFactory, BaseReducerFactory


class SynthesisReducerFactory(SynthesisReducer, BaseReducerFactory):
    composite: Optional[SynthesisComposite] = SynthesisCompositeFactory()


class WeatherReducerFactory(WeatherReducer, BaseReducerFactory):
    composite: Optional[SynthesisComposite] = SynthesisCompositeFactory()
    geo_id: Optional[str] = "id_axis"


class WeatherBuilderFactory(WeatherBuilder, BaseBuilderFactory):
    composite: Optional[SynthesisComposite] = SynthesisCompositeFactory()
    reducer_class: type = WeatherReducerFactory


class TemperatureBuilderFactory(TemperatureBuilder, BaseBuilderFactory):
    composite: Optional[SynthesisComposite] = SynthesisCompositeFactory()
