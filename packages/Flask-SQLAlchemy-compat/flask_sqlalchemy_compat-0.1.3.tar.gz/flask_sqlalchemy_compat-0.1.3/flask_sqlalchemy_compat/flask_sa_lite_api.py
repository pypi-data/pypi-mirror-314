# -*- coding: UTF-8 -*-
"""
APIs of `flask_sqlalchemy_lite`
===============================
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
The proxy wrapper providing the APIs mimicking the behavior of
`flask_sqlalchemy_lite.SQLAlchemy()`. This wrapper is used when users need to support
the features of `flask_sqlalchemy_lite` by using `flask_sqlalchemy`.
"""

import collections.abc
from typing import Union, Optional, Any, Generic, TypeVar, cast

try:
    from typing import Mapping
    from typing import Dict
except ImportError:
    from collections.abc import Mapping
    from builtins import dict as Dict

from typing_extensions import Never, overload

import flask
import sqlalchemy.orm as sa_orm
import sqlalchemy.engine as sa_engine

from flask import g

from .backdict import BackDict
from .protocols import SQLAlchemyProtocol, SQLAlchemyLiteProtocol

from .backends import fsa as _fsa
from .backends import fsa_lite as _fsa_lite
from .backends import is_module_invalid


_SQLAlchemyLiteDB = TypeVar("_SQLAlchemyLiteDB", bound=SQLAlchemyLiteProtocol)
_SQLAlchemyDB_co = TypeVar("_SQLAlchemyDB_co", bound=SQLAlchemyProtocol, covariant=True)

__all__ = ("SQLAlchemyLiteProxy", "as_flask_sqlalchemy_lite")


def _key_engine_to_proxy(key: Optional[str]) -> str:
    """key_back_mapper of `SQLAlchemyLiteProxy.__engines`"""
    return "default" if key is None else key


def _key_proxy_to_engine(key: str) -> Optional[str]:
    """key_back_mapper of `SQLAlchemyLiteProxy.__engines`"""
    return None if key == "default" else key


def _close_sessions(e: Optional[BaseException]) -> None:
    """Close any tracked sessions when the application context ends."""
    sessions: Dict[str, sa_orm.Session] = g.pop("_sqlalchemy_sessions", None)

    if sessions is None:
        return

    for session in sessions.values():
        session.close()


class SQLAlchemyLiteProxy(Generic[_SQLAlchemyDB_co]):
    """Proxy class of `flask_sqlalchemy_lite.SQLAlchemy`.

    This class is a wrapper of the regular SQLAlchemy. By adjusting the behavior of
    the `flask_sqlalchemy.SQLAlchemy`, it can mimic the usage of
    `flask_sqlalchemy_lite.SQLAlchemy`.

    Note that not all the functionalities of `flask_sqlalchemy.SQLAlchemy` can be
    exactly the same as the those of `flask_sqlalchemy_lite.SQLAlchemy`. In specific,
    this proxy will do the following things:

    * Provide a regular session like that of `flask_sqlalchemy_lite.SQLAlchemy`. This
      regular session is managed by this proxy class.
    * Provide other basic methods in `flask_sqlalchemy_lite.SQLAlchemy`. The usages
      would be equivalent but the implmentation is based on `flask_sqlalchemy`.
    * Any functionality that cannot be used will raise a `NotImplementedError`.
    """

    def __init__(self, db: _SQLAlchemyDB_co) -> None:
        """Initialzation.

        Arguments
        ---------
        db: `flask_sqlalchemy.SQLAlchemy`
            The database instance exporting the session and engine instances.

            It is provided by the Flask extensions like `flask_sqlachemy`. This
            wrapper will mimic the behaviors of `flask_sqlalchemy_lite` even if the
            given instance is from the not-lite version.
        """
        self.__db = db

        self.__engines: Optional[BackDict[str, sa_engine.Engine]] = None

    @property
    def db(self) -> _SQLAlchemyDB_co:
        """Property: The `db` instance provided by the Flask SQLAlchemy extension."""
        return self.__db

    @property
    def engines(self) -> Dict[str, sa_engine.Engine]:
        """Property: The same as `flask_sqlalchemy_lite.SQLAlchemy().engines`."""
        if self.__engines is None:
            raise RuntimeError(
                "flask_sqlalchemy_compt: The current Flask app is not registered "
                "with this '{0}' instance. Did you forget to call "
                "`self.init_app()?`".format(self.__class__.__name__)
            )
        return cast(Dict[str, sa_engine.Engine], self.__engines)

    @property
    def engine(self) -> sa_engine.Engine:
        """Property: The same as `flask_sqlalchemy_lite.SQLAlchemy().engine`."""
        return self.__db.engine

    def get_engine(self, name: str = "default") -> sa_engine.Engine:
        """Get a specific engine associated with the current application.

        The `engine` attribute is a shortcut for calling this without an
        argument to get the default engine.

        Arguments
        ---------
        name: `str`
            The name associated with the engine.
        """
        if name == "default":
            return self.__db.engine
        else:
            try:
                return self.engines[name]
            except KeyError as e:
                raise KeyError(
                    "'SQLALCHEMY_ENGINES[\"{0}\"]' was not defined.".format(name)
                ) from e

    def __add_configs(self, app: flask.Flask) -> None:
        """Added configurations to the `app`.

        If the configurations have been configured for `flask_sqlalchemy_lite`, will
        attempt to convert the configurations to the format of `flask_sqlalchemy`.
        """
        if "SQLALCHEMY_DATABASE_URI" in app.config:
            # Do nothing if the configuration is already ready for sqlalchemy
            return
        if "SQLALCHEMY_ENGINES" in app.config:
            # Configurations of flask_sqlalchemy_lite.
            fsa_lite_config = app.config["SQLALCHEMY_ENGINES"]
            if not isinstance(fsa_lite_config, collections.abc.Mapping):
                return
            if "default" not in fsa_lite_config:
                return
            default_url = fsa_lite_config["default"]
            app.config["SQLALCHEMY_DATABASE_URI"] = default_url
            if len(fsa_lite_config) <= 1:
                return
            app.config["SQLALCHEMY_BINDS"] |= {
                engine_name: url for engine_name, url in fsa_lite_config.items()
            }

    def init_app(self, app: flask.Flask) -> None:
        """Register the extension on an application, creating engines from its
        `Flask.config`.

        Arguments
        ---------
        app: `Flask`
            The application to register.
        """
        if "sqlalchemy" not in app.extensions:
            self.__add_configs(app)
            self.__db.init_app(app)
        app.teardown_appcontext(_close_sessions)
        self.__engines = BackDict(
            {},
            self.__get_engines,
            key_mapper=_key_proxy_to_engine,
            key_back_mapper=_key_engine_to_proxy,
        )

    def __get_engines(self) -> Mapping[Optional[str], sa_engine.Engine]:
        """Deferred loader for loading the engines in the app context."""
        return self.__db.engines

    @property
    def sessionmaker(self) -> "sa_orm.sessionmaker[sa_orm.Session]":
        """Property: The same as `flask_sqlalchemy_lite.SQLAlchemy().sessionmaker`.

        The session factory configured for the current application. This can
        be used to create sessions directly, but they will not be closed
        automatically at the end of the application context. Use `session`
        and `get_session` for that.

        This can also be used to update the session options after
        `self.init_app`, by calling its `sa.orm.sessionmaker.configure` method.
        """
        return self.db.session.session_factory

    @property
    def session(self) -> sa_orm.Session:
        """Property: The same as `flask_sqlalchemy_lite.SQLAlchemy().session`.

        The default session for the current application context. It will be
        closed when the context ends.
        """
        return self.get_session()

    def get_session(self, name: str = "default") -> sa_orm.Session:
        """Create a `sa.orm.Session` that will be closed at the end of the application
        context. Repeated calls with the same name within the same application context
        will return the same session.

        The `session` attribute is a shortcut for calling this without an argument to
        get the default session.

        Arguments
        ---------
        `name` A unique name for caching the session.
        """
        sessions: Dict[str, sa_orm.Session] = g.setdefault("_sqlalchemy_sessions", {})

        if name not in sessions:
            sessions[name] = self.sessionmaker()

        return sessions[name]

    @property
    def async_engines(self) -> Never:
        """This property is not implemented by the proxy."""
        raise NotImplementedError(
            "flask_sqlalchemy_compat: Property `async_engines` is purely implemented "
            "in `flask_sqlalchemy_lite`. It is not supported and will not be "
            "supported to call this method while using `flask_sqlalchemy`."
        )

    @property
    def async_engine(self) -> Never:
        """This property is not implemented by the proxy."""
        raise NotImplementedError(
            "flask_sqlalchemy_compat: Property `async_engine` is purely implemented "
            "in `flask_sqlalchemy_lite`. It is not supported and will not be "
            "supported to call this method while using `flask_sqlalchemy`."
        )

    def get_async_engines(self, *args: Any, **kwargs: Any) -> Never:
        """This method is not implemented by the proxy."""
        raise NotImplementedError(
            "flask_sqlalchemy_compat: Method `get_async_engines` iis purely "
            "implemented in `flask_sqlalchemy_lite`. It is not supported and will not "
            "be supported to call this method while using `flask_sqlalchemy`."
        )

    @property
    def async_sessionmaker(self) -> Never:
        """This property is not implemented by the proxy."""
        raise NotImplementedError(
            "flask_sqlalchemy_compat: Property `async_sessionmaker` is purely "
            "implemented in `flask_sqlalchemy_lite`. It is not supported and will "
            "not be supported to call this method while using `flask_sqlalchemy`."
        )

    @property
    def async_session(self) -> Never:
        """This property is not implemented by the proxy."""
        raise NotImplementedError(
            "flask_sqlalchemy_compat: Property `async_session` is purely "
            "implemented in `flask_sqlalchemy_lite`. It is not supported and will "
            "not be supported to call this method while using `flask_sqlalchemy`."
        )

    def get_async_session(self, *args: Any, **kwargs: Any) -> Never:
        """This method is not implemented by the proxy."""
        raise NotImplementedError(
            "flask_sqlalchemy_compat: Method `get_async_session` iis purely "
            "implemented in `flask_sqlalchemy_lite`. It is not supported and will not "
            "be supported to call this method while using `flask_sqlalchemy`."
        )


@overload
def as_flask_sqlalchemy_lite(db: _SQLAlchemyLiteDB) -> _SQLAlchemyLiteDB: ...


@overload
def as_flask_sqlalchemy_lite(
    db: _SQLAlchemyDB_co,
) -> SQLAlchemyLiteProxy[_SQLAlchemyDB_co]: ...


def as_flask_sqlalchemy_lite(
    db: Union[SQLAlchemyProtocol, SQLAlchemyLiteProtocol]
) -> Union[SQLAlchemyLiteProxy[Any], SQLAlchemyLiteProtocol]:
    """Make `db` works as `flask_sqlalchemy_lite`.

    Arguments
    ---------
    db: `flask_sqlalchemy_lite.SQLAlchemy | flask_sqlalchemy.SQLAlchemy`
        The db extension to be wrapped.

    Returns
    -------
    #1: `db: flask_sqlalchemy_lite.SQLAlchemy`
        If `db` is already provided by `flask_sqlalchemy_lite`, return as it is.

    #1: `SQLAlchemyLiteProxy(db)`
        If `db` is provided by `flask_sqlalchemy`, return a proxy wrapper of it.
        This wrapper has the same APIs of `flask_sqlalchemy_lite.SQLAlchemy()` but
        the implementation is based on `flask_sqlalchemy.SQLAlchemy()`.
    """
    if not is_module_invalid(_fsa_lite):
        if isinstance(db, _fsa_lite.SQLAlchemy):
            return db
    if not is_module_invalid(_fsa):
        if isinstance(db, _fsa.SQLAlchemy):
            return SQLAlchemyLiteProxy(db)
    raise TypeError(
        'flask_sqlalchemy_compat: Fail to convert "db" because of either of the '
        'following reasons: (1) Both "flask_sqlalchemy_lite" and "flask_sqlalchemy" '
        'are not installed. (2) "db" is not from "flask_sqlalchemy_lite" or '
        '"flask_sqlalchemy".'
    )
