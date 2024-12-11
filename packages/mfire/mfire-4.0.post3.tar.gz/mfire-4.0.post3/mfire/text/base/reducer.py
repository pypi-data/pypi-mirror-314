from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

import mfire.utils.mfxarray as xr
from mfire.composite.base import BaseComposite, BaseModel, precached_property
from mfire.settings import get_logger
from mfire.utils.date import Datetime, Timedelta

# Logging
LOGGER = get_logger(name="base_reducer.mod", bind="base_reducer")


class BaseReducer(BaseModel, ABC):
    """Classe de base pour implémenter un wind_reducers.
    Il adopte le design pattern du constructeur:
    - il existe un produit "summary" à construire (ici un dictionnaire)
    - une méthode "reset" qui permet de recommencer le processus de construction
    - un ensemble de méthode qui permettent d'ajouter des caractéristiques au "summary"
    - une méthode "compute" qui exécute l'ensemble des étapes et renvoie le "summary"

    '/!\' Dans les classes héritant de BaseReducer,
    il est impératif de détailler au niveau de cette docstring principale
    le schéma du dictionnaire de résumé issu de la méthode "compute".
    """

    data: dict = {}
    geo_id: Optional[str] = None
    reduction: Optional[Union[Dict, List[Dict]]] = None
    composite: Optional[BaseComposite] = None

    @precached_property
    def composite_data(self) -> Optional[Union[xr.DataArray, xr.Dataset]]:
        return self.composite.compute(geo_id=self.geo_id, force=True)

    @abstractmethod
    def _compute(self) -> Union[Dict, List[Dict]]:
        """
        Abstract method in order to make computation and returns the reduced data in
        child classes

        Returns:
            Union[Dict, List[Dict]]: Reduced data
        """

    def compute(self) -> Union[Dict, List[Dict]]:
        """
        Make computation and returns the reduced data.

        Returns:
            Union[Dict, List[Dict]]: Reduced data
        """
        self.reduction = {}
        self.reduction = self._compute()

        self.post_process()

        return self.reduction

    def post_process(self):
        """Make a post-process operation in the reduction."""

    @precached_property
    def times(self) -> List[Datetime]:
        return [Datetime(d) for d in self.composite_data["valid_time"].to_numpy()]

    @precached_property
    def first_time(self) -> Datetime:
        """Returns the first time of the production."""
        if len(self.times) == 1:
            LOGGER.warning("There is only one valid_time to compute weather text.")
            return self.times[0] - Timedelta(hours=1)
        return self.times[0] - (self.times[1] - self.times[0])
