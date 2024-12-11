from __future__ import annotations

import json
from configparser import ConfigParser
from pathlib import Path
from typing import Any, Callable, Hashable, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from dtaidistance import dtw

from mfire.settings import Settings, get_logger
from mfire.settings.constants import LOCALE_DIR, TEMPLATES_FILENAME
from mfire.utils import FormatDict

# Logging
LOGGER = get_logger(name="text.template.mod", bind="text.template")


class Template(str):
    """Template: class extending str type for formating using a custom FormatDict
    (in order to avoid issues when keys are missing).
    >>> s = Template("Ma {b} connait des blagues de {a}, et {c} ?")
    >>> s.format(a="toto", b="tata")
    "Ma tata connait des blagues de toto, et {c} ?"
    >>> s = Template("Bonjour M. {a_prenom} {a_nom}.")
    >>> s.format(a={"nom": "dupont", "prenom": "toto"}, b="tata")
    "Bonjour M. toto dupont."
    """

    def format(self, *args, **kwargs) -> Template:
        try:
            flat_kwargs = pd.json_normalize(kwargs, sep="_").to_dict(orient="records")
            flat_kwargs = flat_kwargs[0]
        except IndexError:
            flat_kwargs = kwargs

        format_dict = FormatDict(flat_kwargs)
        formatted_str = self.format_map(format_dict)
        while (f_str := formatted_str.format_map(format_dict)) != formatted_str:
            formatted_str = f_str

        return formatted_str


class TemplateRetriever:
    """TemplateRetriever : Abstract class for defining a TemplateRetriever.
    It is done to retrieve a string template identified by a key from a file.
    """

    def __init__(self, table: Any):
        """__init__: Initialization method

        Args:
            table (Any): Correspondence table_localisation between keys and values or
            directly the table_localisation
        """
        self.table: Any = table

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.table == other.table

    def __repr__(self) -> str:
        return f"{self.__class__}\n{self.table}"

    @staticmethod
    def read(
        filename: Union[Path, str],
        col: Optional[str] = "template",
        weights: Optional[np.ndarray] = None,
        force_centroid: bool = False,
        **kwargs,
    ) -> Optional[TemplateRetriever]:
        """read_file : reads a templates file and returns the proper corresponding
        TemplateRetriever object.

        Args:
            filename (Union[Path, str]): File containing the template.
            col (Optional[str]): templates column name in a csv file.
            weights (Optional[np.ndarray]): weights if centroids.
            **kwargs: keyword arguments of the file reader used :
                - json : json.load()
                - ini  : ConfigParser().read()
                - csv  : pandas.read_csv()

        Returns:
            Optional[TemplateRetriever]: TemplateRetriever object.
        """
        filename = Path(filename)
        if filename.suffix == ".json":
            return JsonTemplateRetriever.read_file(filename, **kwargs)
        if filename.suffix == ".ini":
            return IniTemplateRetriever.read_file(filename, **kwargs)
        if filename.suffix == ".csv":
            if weights is not None:
                return CentroidTemplateRetriever.read_file(
                    filename, col=col, weights=weights, **kwargs
                )
            index_col = kwargs.pop("index_col", 0)
            tpl_rtr = CsvTemplateRetriever.read_file(
                filename, col=col, index_col=index_col, **kwargs
            )
            if force_centroid or (
                tpl_rtr is not None and "weights" in tpl_rtr.table.index
            ):
                return CentroidTemplateRetriever.read_file(
                    filename, col=col, index_col=index_col, **kwargs
                )
            return tpl_rtr

        return TemplateRetriever.read_file(filename, **kwargs)

    @classmethod
    def read_file(cls, filename: Union[str, Path], **kwargs) -> TemplateRetriever:
        """
        Class method for instantiating an TemplateRetriever out of a file.

        Args:
            filename (Union[str, Path]): Filename

        Returns:
            TemplateRetriever: New cls object
        """
        table = {"filename": Path(filename)}
        table.update(kwargs)
        return cls(table)

    def get(
        self,
        key: Union[Hashable, Sequence[Hashable]],
        default: Optional[str] = None,
        **kwargs,
    ) -> Optional[str]:
        """get: method used to retrieve a specific template identified by a key.

        Args:
            key (Union[Hashable, Sequence[Hashable]]): Key for retrieving our
                template. If the key is a sequence (list, tuple) of keys, then
                we find the template by searching in subdirectories.
            default (Optional[str]): Default value to return if the given
                key is not in self.table_localisation. Defaults to None.

        Returns:
            str: The wanted template
        """
        pop_method = kwargs.get("pop_method") or "random"
        pop_methods = {
            "first": lambda x: x[0],
            "last": lambda x: x[-1],
            "random": Settings().random_choice,
        }

        if key in self.table:
            tpl = self.table[key]
            if isinstance(tpl, str):
                return Template(tpl)
            return Template(pop_methods.get(pop_method, pop_method)(tpl))
        try:
            tpl = self.table
            for element in key:
                tpl = tpl.get(element)
                if tpl is None:
                    return Template(default) if default is not None else None
            if isinstance(tpl, str):
                return Template(tpl)
            return Template(pop_methods.get(pop_method, pop_method)(tpl))
        except (Exception,):
            return Template(default) if default is not None else None

    @staticmethod
    def path_by_name(template: str) -> Path:
        """Returns the template filename according to the language and the given name"""
        return LOCALE_DIR / Settings().language / TEMPLATES_FILENAME[template]

    @staticmethod
    def get_by_name(template: str) -> TemplateRetriever:
        """Returns the template retriever according to the given name"""
        return TemplateRetriever.read(TemplateRetriever.path_by_name(template))

    @staticmethod
    def table_by_name(template: str) -> Any:
        """Returns the template according to the language and the given name"""
        return TemplateRetriever.get_by_name(template).table


class JsonTemplateRetriever(TemplateRetriever):
    """JsonTemplateRetriever : TemplateRetriever from json files.

    Currently used by:
        - mfire.text.comment.comment_builder
    """

    @classmethod
    def read_file(
        cls, filename: Union[str, Path], **kwargs
    ) -> Optional[JsonTemplateRetriever]:
        """read_file : class method for instantiating an JsonTemplateRetriever
        out of a file.

        Args:
            filename (Union[str, Path]): File's name

        Returns:
            JsonTemplateRetriever: New cls object
        """
        try:
            with open(filename, "r") as json_file:
                return cls(json.load(json_file, **kwargs))
        except OSError:
            LOGGER.error(f"Failed to read json template file {filename}", exc_info=True)
            return None


class IniTemplateRetriever(TemplateRetriever):
    """JsonTemplateRetriever : TemplateRetriever from ini files.

    Currently unused.
    """

    @classmethod
    def read_file(
        cls, filename: Union[str, Path], **kwargs
    ) -> Optional[IniTemplateRetriever]:
        """read_file : class method for instantiating an IniTemplateRetriever
        out of a file.

        Args:
            filename (Union[str, Path]): File's name

        Returns:
            IniTemplateRetriever: New cls object
        """
        config = ConfigParser()
        read_ok = config.read(filename, **kwargs)
        if read_ok:
            return cls(config)

        LOGGER.error(
            f"Failed to read ini template file {filename}",
            filename=filename,
            exc_info=True,
        )
        return None

    def get(
        self,
        key: Union[Hashable, Sequence[Hashable]],
        default: Optional[str] = None,
        **kwargs,
    ) -> Optional[str]:
        """get: method used to retrieve a specific template identified by a key.

        Args:
            key (Union[str, tuple[str, str]]): Key for retrieving our
                template. If the key is a string, we search directly in
                the DEFAULT section. Else if it is a tuple of strings, then we
                find the tuple using the usual configparser.get()
            default (str, optional): Default value to return if the given
                key is not in self.table_localisation. Defaults to None.

        Returns:
            str: The wanted template
        """
        if isinstance(key, str):
            key = ("DEFAULT", key)
        try:
            return self.table.get(*key)
        except (Exception,):
            return Template(default) if default is not None else None


class CsvTemplateRetriever(TemplateRetriever):
    """CsvTemplateRetriever : TemplateRetriever for csv files.

    Currently unused.
    """

    def __init__(self, table: pd.DataFrame, col: Optional[str] = "template"):
        """__init__: Initialization method

        Args:
            table (Dict[Hashable, Any]): Correspondance table_localisation
                between Hashable keys and strings (or list of strings).
            col (Optional[str]): Name of the column containing template.
        """
        super().__init__(table=table)
        self.col = col
        if col not in self.table.columns:
            self.col = self.table.columns[0]
            if len(self.table.columns) != 1:
                LOGGER.warning(
                    "Wrong column name given for template retrieving, "
                    "default column taken",
                    given_col=col,
                    selected_col=self.col,
                )
        self.table = self.table[self.col]

    @classmethod
    def read_file(
        cls, filename: Union[str, Path], **kwargs
    ) -> Optional[CsvTemplateRetriever]:
        """read_file : class method for instantiating an CsvTemplateRetriever
        out of a file.

        Args:
            filename (Union[str, Path]): File's name

        Returns:
            CsvTemplateRetriever: New cls object
        """
        try:
            col = kwargs.pop("col", "template")
            return cls(pd.read_csv(filename, **kwargs), col=col)
        except (Exception,):
            LOGGER.error(
                f"Failed to read csv template file {filename}",
                filename=filename,
                exc_info=True,
            )
            return None

    def get(
        self,
        key: Union[Hashable, Sequence[Hashable]],
        default: Optional[str] = None,
        **kwargs,
    ) -> Optional[str]:
        """get: method used to retrieve a specific template identified by a key.

        Args:
            key (Union[Hashable, Tuple]): Key for retrieving our
                template. If the key is a string, we search directly in
                the DEFAULT section. Else if it is a tuple of strings, then we
                find the tuple using the usual configparser.get()
            default (str, optional): Default value to return if the given
                key is not in self.table_localisation. Defaults to None.

        Returns:
            str: The wanted template
        """
        try:
            result = self.table.loc[key]
            if not isinstance(result, (pd.Series, pd.DataFrame)):
                return Template(result)
        except (Exception,):
            pass

        return Template(default) if default is not None else None

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.table.equals(other.table)


class CentroidTemplateRetriever(CsvTemplateRetriever):
    """CentroidTemplateRetriever : TemplateRetriever for csv-centroids files.

    Currently used by:
        - mfire.utils.date : for describing short periods
    """

    def __init__(
        self,
        table: pd.DataFrame,
        col: Optional[str] = "template",
        weights: Optional[Union[list, np.ndarray]] = None,
    ):
        """__init__: Initialization method

        Args:
            table (Dict[Hashable, Any]): Correspondance table_localisation
                between Hashable keys and strings (or list of strings).
            col (Optional[str]): Name of the column containing template
            weights (Optional[list]): Weights to apply. Defaults to None. If None,
                all columns will be given a weight of 1.
        """
        super().__init__(table=table, col=col)
        self.weights = np.array(weights)
        if weights is None:
            self.weights = np.ones(len(self.table.index.names))

    @classmethod
    def read_file(
        cls, filename: Union[str, Path], **kwargs
    ) -> Optional[CentroidTemplateRetriever]:
        """read_file : class method for instantiating an CentroidTemplateRetriever
        out of a file.

        Args:
            filename (Union[str, Path]): File's name

        Returns:
            CentroidTemplateRetriever: New cls object
        """
        try:
            weights = kwargs.pop("weights", None)
            col = kwargs.pop("col", "template")
            index_col = kwargs.pop("index_col", 0)
            df = pd.read_csv(filename, index_col=index_col, **kwargs)
            if "weights" in df.index:
                weights = df.loc["weights"].dropna().values
                df = df.drop("weights").set_index(list(df.columns)[: len(weights)])
            return cls(df, col=col, weights=weights)
        except (Exception,):
            LOGGER.error(
                f"Failed to read csv template file {filename}",
                filename=filename,
                exc_info=True,
            )
            return None

    def get(
        self,
        key: Union[Hashable, Sequence[Hashable]],
        default: Optional[str] = None,
        **kwargs,
    ) -> Union[str, Tuple[str, list]]:
        """get: method used to retrieve a specific template identified by a key.
        It returns the template associated to the nearest centroid of the given key.

        Args:
            key (Union[list, np.ndarray]): Key for retrieving our template.
            default (Optional[str]): Default value to return if the given key is not
                in self.table_localisation. Defaults to None.

        Returns:
            str: The wanted template
        """
        centroids = self.table.index.to_frame().values
        try:
            templates = self.table.values
            dist = np.sum(np.square(self.weights * (centroids - np.array(key))), axis=1)

            key = dist.argmin()
            tpl = Template(templates[key])
        except Exception:
            key, tpl = None, Template(default)
        return (
            tpl
            if not kwargs.get("return_centroid")
            else (tpl, centroids[key].astype("float").tolist())
        )

    def get_by_dtw(
        self,
        key: Union[list, np.ndarray],
        pop_method: Optional[Union[str, Callable]] = "random",
    ) -> dict:
        """Retrieves a specific template identified by a key.

        This method returns the template associated with the nearest centroid
        of the given key using the DTW (Dynamic Time Warping) method.

        Args:
            key (Union[list, np.ndarray]): Key for retrieving the template.
            pop_method (Union[str, Callable[Sequence, str]], optional): Method to use
                if the element retrieved with the key is not a string. It can be a
                string among {"first", "last", "random"}, or it can be a function
                which take the element as input and outputs a str.
                Defaults to "first".

        Returns:
            dict: dict containing the min distance, the path, the template, the centroid
        """

        # Define methods for selecting elements
        pop_methods = {
            "first": lambda x: x[0],
            "last": lambda x: x[-1],
            "random": Settings().random_choice,
        }

        # Get centroids
        centroids = self.table.index.to_frame().values

        # Create a list of data, one for each centroid
        datas = []
        for centroid in centroids:
            data = [x for x in centroid if not pd.isnull(x)]
            datas.append(data)

        # Get templates
        templates = self.table.values

        # Create a dictionary of distances
        distance_dict = {}
        for index, centroid in enumerate(datas):
            distance_dict[tuple(centroid)] = {
                "distance": dtw.distance_fast(
                    np.array(key, dtype=np.double), np.array(centroid, dtype=np.double)
                ),
                "path": dtw.warping_path_fast(
                    np.array(key, dtype=np.double), np.array(centroid, dtype=np.double)
                ),
                "template": Template(
                    pop_methods.get(pop_method, pop_method)(templates[index].split("|"))
                ),
            }

        # Get result
        result = {"distance": np.inf}
        for centroid, value in distance_dict.items():
            if result["distance"] >= value["distance"]:
                result = value | {"centroid": centroid}
        return result

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and np.all(self.weights == other.weights)
