from typing import List

from shapely import box

from mfire.mask.processor import GridProcessor, Processor
from tests.factories import Factory


class ProcessorFactory(Factory, Processor):
    pass


class GridProcessorFactory(GridProcessor):
    features: List[dict] = [
        {
            "id": "id1",
            "properties": {"name": "area_name1"},
            "geometry": box(-4.04, 47.04, -4, 47),
        }
    ]
    grid_name: str = "franxl1s100"
