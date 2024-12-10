# -*- coding: UTF-8 -*-
"""
Auto
======
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
Methods used for creating the `SQLAlchemy` extension in the compatible mode.
The compatiblity is supported by the automatic falling-back strategy. For example,

1. `get_flask_sqlalchemy_lite(...)` is a method returning the db extesnion of
   `flask_sqlalchemy_lite.SQLAlchemy()`.
2. If `flask_sqlalchemy_lite` is not installed but `flask_sqlalchemy` is installed,
   will return a db extension with a backend of `flask_sqlalchemy.SQLAlchemy()`. This
   wrapped extension will mimic the behaviors of `flask_sqlalchemy_lite.SQLAlchemy()`.
3. If both `flask_sqlalchemy` and `flask_sqlalchemy_lite` are not installed, raise
   a `ModuleNotFoundError`.
"""

import collections.abc

from typing import TYPE_CHECKING, cast
from typing import Optional, TypeVar, Any

try:
    from typing import Mapping
    from typing import Tuple, Type
except ImportError:
    from collections.abc import Mapping
    from builtins import tuple as Tuple, type as Type

import sqlalchemy.orm as sa_orm

from flask import Flask

from .backends import fsa as _fsa
from .backends import fsa_lite as _fsa_lite
from .backends import is_module_invalid

from .flask_sa_api import as_flask_sqlalchemy
from .flask_sa_lite_api import as_flask_sqlalchemy_lite


if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy
    from flask_sqlalchemy_lite import SQLAlchemy as SQLAlchemyLite
else:

    class SQLAlchemyLite:
        """Place holder of `flask_sqlalchemy_lite.SQLAlchemy`"""

    class SQLAlchemy:
        """Place holder of `flask_sqlalchemy_lite.SQLAlchemy`"""


_ModelLite = TypeVar("_ModelLite", bound=sa_orm.DeclarativeBase, covariant=True)

__all__ = ("get_flask_sqlalchemy_lite", "get_flask_sqlalchemy")


def get_flask_sqlalchemy_lite(
    model_class: Type[_ModelLite],
    app: Optional[Flask] = None,
    engine_options: Optional[Mapping[str, Any]] = None,
    session_options: Optional[Mapping[str, Any]] = None,
) -> Tuple[SQLAlchemyLite, Type[_ModelLite]]:
    """Get the Flask SQLAlchemy Lite DB instance in the compatible mode.

    This method will attempt to get the `flask_sqlalchemy_lite.SQLAlchemy` DB instance.
    If the attempt fails (package is not installed), will fallback to use
    `flask_sqlalchemy.SQLAlchemy` to imitate the interfaces of
    `flask_sqlalchemy_lite.SQLAlchemy`.

    Arguments
    ---------
    model_class: `sa.orm.DeclarativeBase`
        The base model type applied to the whole database. If `flask_sqlalchemy_lite`
        is available, this type will be directly forwarded as it is. It will not
        modify anything. However, if the db instance fallback to the version provided
        by `flask_sqlalchemy`, this type will be used for creating the db-specific
        model type.

    app: `Flask | None`
        Call `init_app` on this Flask application. If not specified, will not call
        `init_app`.

    engine_options: `Mapping[str, Any]`
        Default arguments passed to `sqlalchemy.create_engine` for each configured
        engine.

    session_options: `Mapping[str, Any]`
        Arguments to configure `sessionmaker` with.

    Returns
    -------
    #1: `flask_sqlalchemy_lite.SQLAlchemy`
        The SQLAlchemy Lite extension instance. It will be an instance of
        `flask_sqlalchemy_lite.SQLAlchemy` if the package is available.

        If the package is not available, will attempt to return a
        `SQLAlchemyLiteProxy[flask_sqlalchemy.SQLAlchemy]` instance. However, this
        returned value is still notated by `flask_sqlalchemy_lite.SQLAlchemy`, which
        indicates that users should use `flask_sqlalchemy_lite` to develop their
        codes, while making this returned value as a falling back option.

    #2: `model_class (Type[sa.orm.DeclarativeBase])`:
        If `#1` is `flask_sqlalchemy_lite.SQLAlchemy`, will return `model_class`
        directly.

        If `#1` is `SQLAlchemyLiteProxy[flask_sqlalchemy.SQLAlchemy]`, will return
        `#1.Model` as the falling back option.
    """
    if app is not None and not isinstance(app, Flask):
        raise TypeError(
            'flask_sqlalchemy_compat: The argument "app" needs to be `None` or a '
            "Flask application instance."
        )
    engine_options = (
        dict(engine_options)
        if isinstance(engine_options, collections.abc.Mapping)
        else None
    )
    session_options = (
        dict(session_options)
        if isinstance(session_options, collections.abc.Mapping)
        else None
    )
    if not is_module_invalid(_fsa_lite):
        return (
            _fsa_lite.SQLAlchemy(
                app, engine_options=engine_options, session_options=session_options
            ),
            model_class,
        )
    if not is_module_invalid(_fsa):
        _db = _fsa.SQLAlchemy(
            model_class=model_class,
            session_options=session_options,
            engine_options=engine_options,
        )
        _wrap = as_flask_sqlalchemy_lite(_db)
        if app is not None:
            _wrap.init_app(app)
        return cast(Any, _wrap), cast(Any, _db.Model)
    raise ModuleNotFoundError(
        'flask_sqlalchemy_compat: Both "flask_sqlalchemy_lite" and '
        '"flask_sqlalchemy" are not installed, cannot get the SQLAlchemy or its '
        "proxy db instance."
    )


def get_flask_sqlalchemy(
    model_class: Type[sa_orm.DeclarativeBase],
    app: Optional[Flask] = None,
    engine_options: Optional[Mapping[str, Any]] = None,
    session_options: Optional[Mapping[str, Any]] = None,
) -> SQLAlchemy:
    """Get the Flask SQLAlchemy DB instance in the compatible mode.

    This method will attempt to get the `flask_sqlalchemy.SQLAlchemy` DB instance.
    If the attempt fails (package is not installed), will fallback to use
    `flask_sqlalchemy_lite.SQLAlchemy` to imitate the interfaces of
    `flask_sqlalchemy.SQLAlchemy`.

    Arguments
    ---------
    model_class: `sa.orm.DeclarativeBase`
        The base model type applied to the whole database. If `flask_sqlalchemy`
        is available, this type will be used as `model_class` argument for creating
        the db-specific base model type. However, if the db instance fallback to the
        version provided by `flask_sqlalchemy_lite`, this type will be modified inplace
        to imitate the behavior of `flask_sqlalchemy.SQLAlchemy().Model`.

    app: `Flask | None`
        Call `init_app` on this Flask application. If not specified, will not call
        `init_app`.

    engine_options: `Mapping[str, Any]`
        Default arguments passed to `sqlalchemy.create_engine` for each configured
        engine.

    session_options: `Mapping[str, Any]`
        Arguments to configure `sessionmaker` with.

    Returns
    -------
    #1: `flask_sqlalchemy.SQLAlchemy`
        The SQLAlchemy extension instance. It will be an instance of
        `flask_sqlalchemy.SQLAlchemy` if the package is available.

        If the package is not available, will attempt to return a
        `SQLAlchemyProxy[flask_sqlalchemy_lite.SQLAlchemy]` instance. However, this
        returned value is still notated by `flask_sqlalchemy.SQLAlchemy`, which
        indicates that users should use `flask_sqlalchemy` to develop their
        codes, while making this returned value as a falling back option.
    """
    if app is not None and not isinstance(app, Flask):
        raise TypeError(
            'flask_sqlalchemy_compat: The argument "app" needs to be `None` or a '
            "Flask application instance."
        )
    engine_options = (
        dict(engine_options)
        if isinstance(engine_options, collections.abc.Mapping)
        else None
    )
    session_options = (
        dict(session_options)
        if isinstance(session_options, collections.abc.Mapping)
        else None
    )
    if not is_module_invalid(_fsa):
        return _fsa.SQLAlchemy(
            model_class=model_class,
            session_options=session_options,
            engine_options=engine_options,
        )
    if not is_module_invalid(_fsa_lite):
        _db = _fsa_lite.SQLAlchemy(
            app, engine_options=engine_options, session_options=session_options
        )
        _wrap = as_flask_sqlalchemy(_db, model_class=model_class)
        if app is not None:
            _wrap.init_app(app)
        return cast(Any, _wrap)
    raise ModuleNotFoundError(
        'flask_sqlalchemy_compat: Both "flask_sqlalchemy" and '
        '"flask_sqlalchemy_lite" are not installed, cannot get the SQLAlchemy or its '
        "proxy db instance."
    )
