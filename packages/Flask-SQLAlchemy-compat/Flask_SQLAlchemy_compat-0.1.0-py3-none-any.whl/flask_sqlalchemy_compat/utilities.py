# -*- coding: UTF-8 -*-
"""
Utilities
=========
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
The extra functionalities used for hooking the original SQLAlchemy extensions. The
extensions need to be hooked because some extra functionalities may need to be
provided.
"""

import re
import functools

from typing import Union, Optional, Any, TypeVar, cast

try:
    from typing import Sequence, Mapping, Callable
    from typing import Dict, Type
except ImportError:
    from collections.abc import Sequence, Mapping, Callable
    from builtins import dict as Dict, type as Type

from typing_extensions import Concatenate, ParamSpec, Self

import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import sqlalchemy.orm as sa_orm
from flask import current_app
from flask.globals import app_ctx

from .protocols import SQLAlchemyProtocol, SQLAlchemyLiteProtocol


P = ParamSpec("P")
T = TypeVar("T")
_Type = TypeVar("_Type", bound=Type)

_Model_contra = TypeVar(
    "_Model_contra",
    bound=Union[sa_orm.DeclarativeBase, sa_orm.DeclarativeBaseNoMeta],
    contravariant=True,
)

__all__ = (
    "hook_classmethod",
    "hook_base_model",
    "apply_to_engines",
    "clone_method",
    "get_app_ctx_id",
    "QueryGetter",
    "TableNameGetter",
)


class DBNotReadyError(RuntimeError):
    """Exception raised by QueryGetter.

    Will raise this exception if the `QueryGetter` is accessed before passed to the
    SQLAlchemy extension or using `init_app()`.
    """

    pass


def hook_classmethod(
    cls_method: Callable[P, T],
    hook_before: Optional[Callable[Concatenate[_Type, P], None]] = None,
    hook_after: Optional[Callable[Concatenate[_Type, P], None]] = None,
) -> Callable[P, T]:
    """Hook a class method.

    Arguments
    ---------
    cls_method: `(**P) -> T`
        A class method that is hooked. This is the bounded version of the class
        method, where the first argument `cls` has been implied and not included
        in the spec `P`.

    hook_before: `None | (type, **P) -> T`
        The hook that will be run before this class method.

    hook_after: `(type, **P) -> T`
        The hook that will be run after this class method.
    """

    if hook_before is None and hook_after is None:
        return cls_method

    prototype = getattr(cls_method, "__func__")

    if hook_before is not None and hook_after is not None:

        @functools.wraps(prototype)
        def hooked(cls: _Type, *args: P.args, **kwargs: P.kwargs) -> T:
            hook_before(cls, *args, **kwargs)
            res = prototype(cls, *args, **kwargs)
            hook_after(cls, *args, **kwargs)
            return res

    elif hook_before is not None:

        @functools.wraps(prototype)
        def hooked(cls: _Type, *args: P.args, **kwargs: P.kwargs) -> T:
            hook_before(cls, *args, **kwargs)
            res = prototype(cls, *args, **kwargs)
            return res

    elif hook_after is not None:

        @functools.wraps(prototype)
        def hooked(cls: _Type, *args: P.args, **kwargs: P.kwargs) -> T:
            res = prototype(cls, *args, **kwargs)
            hook_after(cls, *args, **kwargs)
            return res

    else:
        raise TypeError(
            "flask_sqlalchemy_compat: either the argument hook_before or hook_after "
            "needs to be specified."
        )

    return cast(Callable[P, T], classmethod(hooked))


def _hook_base_model_subclass(cls, *args: Any, **kwargs: Any) -> None:
    """The hook used in `hook_base_model`."""
    try:
        _attr = getattr(cls, "__tablename__", None)
    except sa_exc.ArgumentError:
        pass
    else:
        if _attr is None:
            name = TableNameGetter.calc_auto_table_name(cls.__name__)
            cls.__tablename__ = name
    try:
        _attr = getattr(cls, "query", None)
    except (sa_exc.ArgumentError, DBNotReadyError):
        pass
    else:
        if _attr is None:
            cls.query = QueryGetter()
    try:
        _attr = getattr(cls, "query_cls", None)
    except sa_exc.ArgumentError:
        pass
    else:
        if _attr is None:
            cls.query_cls = sa_orm.Query


def hook_base_model(
    cls: Type[_Model_contra],
    db: Union[SQLAlchemyProtocol, SQLAlchemyLiteProtocol],
) -> Type[_Model_contra]:
    """Add hooks to the given Model class. This hook will synthesize the
    `__tablename__`, `query` and `query_cls` properties if any of them is not
    specified in the subclass.

    Arguments
    ---------
    cls: `Type[DeclarativeBase] | Type[DeclarativeBaseNoMeta]`
        The class to be hooked.

    db: `flask_sqlalchemy.SQLAlchemy | flask_sqlalchemy_lite.SQLAlchemy`
        The db instance used for providing the session.
    """

    try:
        _attr = getattr(cls, "__fsa__", None)
    except sa_exc.ArgumentError:
        pass
    else:
        if _attr is None:
            setattr(cls, "__fsa__", db)

    cls.__init_subclass__ = hook_classmethod(
        cls.__init_subclass__, hook_before=_hook_base_model_subclass
    )
    return cls


def apply_to_engines(
    func: Callable[[sa.Engine], None],
    bind_key: Union[str, None, Sequence[Union[str, None]]],
    engines: Mapping[str, sa.Engine],
    default_engine: sa.Engine,
) -> None:
    """Apply a function to one or multiple engines.

    The given `func` is a function designed to be applied to a single engine. This
    method defines the logics of how to apply `func` to multiple engines.

    Arguments
    ---------
    func: `(sa.Engine) -> None`
        The function to be applied to a single engine.

    bind_key: `str | None | Sequence[str | None]`
        The name(s) of the engines where the `func` will be applied to.

    engines: `Mapping[str, sa.Engine]`
        The collection of all registered engines. If `bind_key` is `__all__`, will
        apply `func` to all engines in this list.

    default_engine: `sa.Engine`
        The default engine. It should be the same as `engines["default"]`.
    """
    if bind_key is None:
        func(default_engine)
        return
    if isinstance(bind_key, str):
        if bind_key == "__all__":
            for engine in engines.values():
                func(engine)
            return
        elif bind_key == "default":
            func(default_engine)
            return
        func(engines[bind_key])
        return
    for name in bind_key:
        if name is None:
            func(default_engine)
            return
        func(engines[name])


def clone_method(
    method: Callable[Concatenate[P], Any],
) -> Callable[[Callable[Concatenate[Any, P], T]], Callable[Concatenate[Any, P], T]]:
    """A decorator for modifying the static type hint of a method by cloning the
    signature of another method.

    This decorator should be only used for cloning the regular method. It is not
    suitable for classmethod, staticmethod or regular functions.

    Arguments
    ---------
    method: `(**P) -> Any`
        The original method providing the signature to be cloned.

    Returns
    -------
    #1: `((self, **P) -> T) -> ((self, **P) -> T)`
        A wrapper that forward a function as it is directly but the signature of the
        function will be consistent with the argument `method`.

        The input signature will be copied from `method`. But the output value will
        be determined by the wrapped method.
    """

    def wrapper(
        func: Callable[Concatenate[Any, P], T]
    ) -> Callable[Concatenate[Any, P], T]:
        _doc = func.__doc__
        _func = functools.wraps(method)(func)
        _func.__doc__ = "{0}\n\nOriginal Method\n---------------\n\n{1}".format(
            _doc, func.__doc__
        )
        return _func

    return wrapper


def get_app_ctx_id() -> int:
    """Get the ID of the current Flask app context object."""
    return id(getattr(app_ctx, "_get_current_object"))


class QueryGetter:
    """The getter of the `query` property.

    Use this descriptor like this:
    ``` python
    class Base:
        query = QueryGetter()

    class NewModel(Base): ...
    ```
    It will mimic the behavior of `flask_sqlalchemy`. Using
    ``` python
    NewModel.query.filter(...).all()
    ```
    will be equivalent with
    ``` python
    db.session.query(NewModel).filter(...).all()
    ```
    """

    def __init__(self) -> None:
        """Initialization."""
        self.__db: Optional[Union[SQLAlchemyProtocol, SQLAlchemyLiteProtocol]] = None

    def __get_session(
        self, obj_cls: Type[_Model_contra]
    ) -> Union[sa_orm.Session, sa_orm.scoped_session[sa_orm.Session]]:
        if self.__db is not None:
            return self.__db.session
        __db = getattr(obj_cls, "__fsa__")
        if __db is None:
            raise DBNotReadyError(
                "flask_sqlalchemy_compat: Cannot detect the DB reference. Maybe the "
                "model has not been passed to a `flask_sqlalchemy.SQLAlchemy` object "
                "or its proxy."
            )
        if __db is not current_app.extensions.get("sqlalchemy"):
            raise DBNotReadyError(
                "flask_sqlalchemy_compat: Cannot use `query` before registering the "
                "app by `init_app(...)`."
            )
        self.__db = __db
        return __db.session

    def __get__(
        self: Self,
        obj: Optional[_Model_contra],
        obj_cls: Optional[Type[_Model_contra]] = None,
    ) -> sa_orm.Query[_Model_contra]:
        """Return the query object from the current class."""
        if obj_cls is not None:
            cls = obj_cls
        elif obj is not None:
            cls = obj.__class__
        else:
            raise ValueError("flask_sqlalchemy_compat: Unknown Query instance.")
        return self.__get_session(cls).query(cls)


class TableNameGetter:
    """The getter of the `__tablename__` property.

    Use this descriptor like this:
    ``` python
    class Base:
        __tablename__ = TableNameGetter()

    class NewModel(Base): ...
    ```
    or like this:
    ``` python
    class NewModel(Base):
        __tablename__ = TableNameGetter()
    ```
    It will
    1. Prevent users to modify `__tablename__` of an instance of the model class.
    2. Return an automatically synthesized table name if it is not defined.
    """

    REGEX_UPPER_TO_UNDERSCORE = re.compile(r"(?<=\w)(?=[A-Z])")
    REGEX_UNKNOWN_TO_UNDERSCORE = re.compile(r"[^\w_]")

    def __init__(self) -> None:
        """Initialization."""
        self.registry: Dict[int, str] = dict()

    @classmethod
    def calc_auto_table_name(cls, name: str) -> str:
        """Calculate the auto-generated table from from a class name."""
        name = re.sub(cls.REGEX_UPPER_TO_UNDERSCORE, "_", name).lower()
        name = re.sub(cls.REGEX_UNKNOWN_TO_UNDERSCORE, "_", name)
        return name

    def get_auto_table_name(self, obj_cls: Type[_Model_contra]) -> str:
        """Use this method to synthesize the __tablename__ when the value is not
        manually configured."""
        obj_cls_id = id(obj_cls)
        _name = self.registry.get(obj_cls_id)
        if _name is not None:
            return _name
        name = self.calc_auto_table_name(obj_cls.__name__)
        self.registry[id(obj_cls)] = name
        return name

    def __get__(
        self: Self,
        obj: Optional[_Model_contra],
        obj_cls: Optional[Type[_Model_contra]] = None,
    ) -> str:
        """Return the automatically synthesized table name."""
        if obj_cls is not None:
            return self.get_auto_table_name(obj_cls)
        if obj is not None:
            return self.get_auto_table_name(obj.__class__)
        raise ValueError("flask_sqlalchemy_compat: Unknown __tablename__.")
