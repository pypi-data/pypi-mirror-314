from __future__ import annotations

from typing import Optional, Union

import numpy as np
import xarray as xr
from pandas.core.dtypes.common import is_bool_dtype, is_numeric_dtype

# Alias definitions
Coordinates = xr.Coordinates
DataArray = xr.DataArray
Dataset = xr.Dataset
merge = xr.merge
testing = xr.testing
MergeError = xr.MergeError

# Function aliases
align = xr.align
apply_ufunc = xr.apply_ufunc
broadcast = xr.broadcast
concat = xr.concat
full_like = xr.full_like
ones_like = xr.ones_like
open_dataarray = xr.open_dataarray
open_dataset = xr.open_dataset
set_options = xr.set_options
where = xr.where
zeros_like = xr.zeros_like


@xr.register_dataarray_accessor("wheretype")
class TypeAccessor:
    """
    Custom accessor that adds a 'wheretype' attribute to DataArrays
    and provides methods to convert the result of 'where' to the desired type.
    """

    def __init__(self, xarray_obj):
        self._obj = xarray_obj

    def bool(self, *args, **kwargs):
        """
        Converts the result of 'where' to boolean type.

        Parameters:
            *args: Arguments to be passed to the 'where' method.
            **kwargs: Keyword arguments to be passed to the 'where' method.

        Returns:
            DataArray: A boolean DataArray.
        """
        return ~self._obj.where(*args, **kwargs).isnull()

    def f32(self, *args, **kwargs):
        """
        Converts the result of 'where' to float32 type.

        Parameters:
            *args: Arguments to be passed to the 'where' method.
            **kwargs: Keyword arguments to be passed to the 'where' method.

        Returns:
            DataArray: A float32 DataArray.
        """
        return self._obj.where(*args, **kwargs).astype("float32", copy=False)


@xr.register_dataarray_accessor("mask")
class MaskAccessor:
    """
    Custom accessor that adds a 'mask' attribute to DataArrays.
    """

    def __init__(self, xarray_obj: xr.DataArray):
        if not is_numeric_dtype(xarray_obj) and not is_bool_dtype(xarray_obj):
            raise ValueError(
                "Dtype for DataArray of MaskAccessor must be numeric or boolean"
            )
        self._obj = xarray_obj > 0

    @property
    def bool(self) -> xr.DataArray:
        """
        Returns the mask as a boolean DataArray.
        """
        return self._obj

    @property
    def bool_dropped(self) -> xr.DataArray:
        """
        Returns the mask as a boolean DataArray with dropped dimensions where the mask
        is False.
        """
        return self._obj.where(self._obj, drop=True)

    @property
    def f32(self) -> xr.DataArray:
        """
        Returns the mask as a float32 DataArray.
        """
        return self._obj.where(self._obj).astype("float32", copy=False)

    @property
    def f32_dropped(self):
        """
        Returns the mask as a float32 DataArray with dropped dimensions where the mask
        is False.
        """
        return self._obj.where(self._obj, drop=True).astype("float32", copy=False)

    def union(self, other: Union[xr.DataArray, MaskAccessor]) -> MaskAccessor:
        """
        Make union of two masks by filling in missing values with the other mask.

        Args:
            other (Union[xr.DataArray, MaskAccessor]): The other mask to make the union.

        Returns:
            The union of the two masks.
        """
        if isinstance(other, xr.DataArray):
            other = other.mask

        return MaskAccessor(np.logical_or(self._obj, other.bool))

    @staticmethod
    def unions(*args: Union[xr.DataArray, MaskAccessor]):
        """
        Make unions of several masks.

        Args:
            *args (Union[xr.DataArray, MaskAccessor]): Masks to make the union.

        Returns:
            The union of all masks.
        """
        if len(args) == 0:
            return []

        result = args[0]
        if isinstance(result, xr.DataArray):
            result = result.mask

        for arg in args[1:]:
            result = result.union(arg)
        return result

    @staticmethod
    def sum(a: Optional[xr.DataArray], b: Optional[xr.DataArray]) -> xr.DataArray:
        if a is None:
            return b
        if b is None:
            return a
        return ((a.fillna(0) + b.fillna(0)) > 0).where(a.notnull() | b.notnull())


@xr.register_dataarray_accessor("masked_data")
class MaskedDataAccessor:
    """
    Custom accessor that adds a 'masked_data' attribute to DataArrays.
    """

    def __init__(self, xarray_obj: xr.DataArray):
        if not is_numeric_dtype(xarray_obj):
            raise ValueError(
                "Dtype for DataArray of MaskedDataAccessor must be numeric"
            )
        self._obj = xarray_obj.where(
            np.logical_or(xarray_obj.isnull(), xarray_obj == 0), 1.0
        ).astype("float32", copy=False)

    @property
    def f32(self) -> xr.DataArray:
        """
        Returns the object as a float32 DataArray.
        """
        return self._obj

    @property
    def f32_dropped(self):
        """
        Returns the object as a float32 DataArray with dropped dimensions where the data
        is False.
        """
        return self._obj.where(self._obj > 0, drop=True)

    def union(
        self, other: Union[xr.DataArray, MaskedDataAccessor]
    ) -> MaskedDataAccessor:
        """
        Make union of two objects

        Args:
            other (Union[xr.DataArray, MaskedDataAccessor]): The other object to make
                the union.

        Returns:
            The union of the two objects.
        """
        if isinstance(other, xr.DataArray):
            other = other.masked_data

        other = other.f32
        result = xr.where(self._obj == 0.0, other.fillna(0), self._obj)
        return result.where(result.notnull(), other).masked_data

    @staticmethod
    def unions(*args: Union[xr.DataArray, MaskedDataAccessor]):
        """
        Make union of several objects

        Args:
            args (Union[xr.DataArray, MaskedDataAccessor]): Objects to make the union.

        Returns:
            The union of all objects.
        """
        if len(args) == 0:
            return []

        result = args[0]
        if isinstance(result, xr.DataArray):
            result = result.masked_data

        for arg in args[1:]:
            result = result.union(arg)
        return result
