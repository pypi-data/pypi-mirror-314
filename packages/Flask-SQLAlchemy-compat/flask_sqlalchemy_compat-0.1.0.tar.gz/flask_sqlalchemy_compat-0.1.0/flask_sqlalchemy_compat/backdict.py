# -*- coding: UTF-8 -*-
"""
BackDict
========
@ Flask SQLAlchemy Compat

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
The implementation of a modified `dict`. The usage of `BackDict` is like that of a two-
level `collections.ChainMap`. It is used by `flask_sa_lite_api` for supporting the
mapping strategy from the properties of `flask_sqlalchemy.SQLAlchemy()` to
`flask_sqlalchemy_lite.SQLAlchemy()`.
"""

import sys
import itertools
import collections.abc

from typing import Union, Any, Generic, TypeVar

try:
    from typing import Mapping, Iterator, Callable
except ImportError:
    from collections.abc import Mapping, Iterator, Callable

from typing_extensions import Self


K = TypeVar("K")
K2 = TypeVar("K2")
V = TypeVar("V")
V_co = TypeVar("V_co", covariant=True)
S = TypeVar("S")


if sys.version_info < (3, 9):
    from collections import UserDict as _UserDict

    class _Mapping(collections.abc.Mapping, Generic[K, V]):
        """Dummy Compatible version of typehint available `Mapping`."""

    class UserDict(_UserDict, Generic[K, V]):
        """Compatible version of UserDict from python>=3.9.

        This modified `UserDict` is used for supporting `UserDict[Key, Val]` interface
        when using python<=3.8.
        """

        pass

else:
    from collections import UserDict
    from collections.abc import Mapping as _Mapping


__all__ = ("BackDictView", "BackDict")


class BackDictView(_Mapping[K, V]):
    """Internal class. The read-only proxy used by `MappingView` of `BackDict`."""

    def __init__(
        self,
        data: Mapping[K, V],
        back_data: Mapping[K2, V],
        key_mapper: Callable[[K], K2],
        key_back_mapper: Callable[[K2], K],
    ) -> None:
        """Initialization.

        This class should be initialized by methods of `BackDict`. Users should not
        explicitly initialize it.

        Arguments
        ---------
        data: `Mapping[K, T]`
            Mutable data internal storage of `BackDict`.

        back_data: `Mapping[K2, T]`
            Backup immutable data internal storage of `BackDict`.

        key_mapper:
            Use this mapper to convert `K` to `K2` when the key is not found in `data`.

        key_back_mapper:
            Use this mapper to convert `K2` to `K` when the key needs to be listed to
            users.
        """
        self.__keys = set(data.keys()).union(
            key_back_mapper(key) for key in back_data.keys()
        )
        self.__data = data
        self.__back_data = back_data
        self.__key_mapper = key_mapper

    def __len__(self) -> int:
        return len(self.__keys)

    def __iter__(self) -> Iterator[K]:
        return iter(self.__keys)

    def __contains__(self, key: Any) -> bool:
        if key in self.__data:
            return True
        return key in self.__back_data

    def __getitem__(self, key: K) -> V:
        if key in self.__data:
            return self.__data[key]
        return self.__back_data[self.__key_mapper(key)]


class BackDict(UserDict[K, V]):
    """Dictionary with a falling-back level.

    A two-level chain map supporting the following feature:
    1. The first level `data` is a readable and writable domain. Any modification of
       this dictionary will take effects on the `data` domain.
    2. The second level `back_dict` is a read-only domain. When iterating or locating
       values of this dictionary, the value will be searched in the `data` domain
       first. If it is not found, will return the value in `back_dict` domain. Since
       the modifications of the dictionary will only take effects on the `data` domain,
       this second-level domain will not change.
    3. The second-level dictionary can have different keyword types. compared to the
       `data` domain. Users need to provide a `key_mapper` and its inverse operator
       `key_back_mapper` to support this feature.
    """

    def __init__(
        self,
        data: Mapping[K, V],
        back_dict: Mapping[K2, V],
        key_mapper: Callable[[K], K2],
        key_back_mapper: Callable[[K2], K],
    ) -> None:
        """Initialization.

        Arguments
        ---------
        data: `Mapping[K, T]`
            Mutable data internal storage of `BackDict`.

        back_data: `Mapping[K2, T]`
            Backup immutable data internal storage of `BackDict`.

        key_mapper:
            Use this mapper to convert `K` to `K2` when the key is not found in `data`.

        key_back_mapper:
            Use this mapper to convert `K2` to `K` when the key needs to be listed to
            users.
        """
        super().__init__(data)
        self.__back_dict = back_dict
        self.__key_mapper = key_mapper
        self.__key_back_mapper = key_back_mapper
        self.__view = BackDictView(
            data, back_dict, key_mapper=key_mapper, key_back_mapper=key_back_mapper
        )

    def __repr__(self) -> str:
        return "{{{0}}}".format(
            ", ".join("{0}: {1}".format(repr(key), repr(self[key])) for key in self)
        )

    def __str__(self) -> str:
        return "{{{0}}}".format(
            ", ".join("{0}: {1}".format(repr(key), str(self[key])) for key in self)
        )

    def __len__(self) -> int:
        """Number of items in this `LRUDict`."""
        return len(set(self.data).union(self.__back_dict))

    def __contains__(self, key: Any) -> bool:
        if key in self.data:
            return True
        return key in self.__back_dict

    def __iter__(self) -> Iterator[K]:
        keys = iter(
            set(self.data).union(
                self.__key_back_mapper(key) for key in self.__back_dict
            )
        )
        return keys

    def __getitem__(self, key: K) -> V:
        if key in self.data:
            return self.data[key]
        return self.__back_dict[self.__key_mapper(key)]

    # Inherit from the Dict
    def __or__(self: Self, val: Mapping[K, V]) -> Self:
        """Create a new `BackDict` with the merged keys and values of this `BackDict`
        and other, which can be an arbitrary mapping type. The values of other take
        priority when the keys are shared.
        """
        return self.__class__(
            data=dict(itertools.chain(self.data.items(), val.items())),
            back_dict=self.__back_dict,
            key_mapper=self.__key_mapper,
            key_back_mapper=self.__key_back_mapper,
        )

    def __ror__(self, val: Mapping[K, V]) -> Self:
        """Create a new `BackDict` with the merged keys and values of this `BackDict`
        and other, which can be an arbitrary mapping type. The values of this
        `BackDict` take priority when the keys are shared.

        Note that this method is used only when `val` does not implement the `__or__`
        operator.
        """
        return self.__class__(
            data=dict(itertools.chain(val.items(), self.items())),
            back_dict=self.__back_dict,
            key_mapper=self.__key_mapper,
            key_back_mapper=self.__key_back_mapper,
        )

    def get(self, key: K, default: S = None) -> Union[V, S]:
        """Get a value from the dictionary with a default value provided."""
        if key in self.data:
            return self.data[key]
        return self.__back_dict.get(self.__key_mapper(key), default=default)

    def copy(self) -> Self:
        """Make a shallow copy of this `LRUDict`."""
        res = self.__class__(
            data=self.data,
            back_dict=self.__back_dict,
            key_mapper=self.__key_mapper,
            key_back_mapper=self.__key_back_mapper,
        )
        return res

    def keys(self):
        """`LRUDict(...).keys()` -> a set-like object providing a view on
        `LRUDict`'s keys."""
        return collections.abc.KeysView(self.__view)

    def items(self):
        """`LRUDict(...).items()` -> a set-like object providing a view on
        `LRUDict`'s items."""
        return collections.abc.ItemsView(self.__view)

    def values(self):
        """`LRUDict(...).values()` -> an object providing a view on `LRUDict`'s
        values."""
        return collections.abc.ValuesView(self.__view)
