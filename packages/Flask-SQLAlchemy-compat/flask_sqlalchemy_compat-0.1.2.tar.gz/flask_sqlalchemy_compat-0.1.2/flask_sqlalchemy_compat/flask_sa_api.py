# -*- coding: UTF-8 -*-
"""
APIs of `flask_sqlalchemy`
==========================
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
`flask_sqlalchemy.SQLAlchemy()`. This wrapper is used when users need to support the
features of `flask_sqlalchemy` by using `flask_sqlalchemy_lite`.
"""

import functools
import collections
import collections.abc

from typing import Union, Optional, Any, Generic, TypeVar, cast

try:
    from typing import Sequence, Callable, MutableMapping
    from typing import Tuple, Dict, Type
except ImportError:
    from collections.abc import Sequence, Callable, MutableMapping
    from builtins import tuple as Tuple, dict as Dict, type as Type

from typing_extensions import (
    Concatenate,
    Never,
    ParamSpec,
    TypeVarTuple,
    overload,
)

import flask
import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import sqlalchemy.orm as sa_orm
import sqlalchemy.engine as sa_engine
import sqlalchemy.event as sa_event

from sqlalchemy.orm.session import _EntityBindKey, _PKIdentityArgument

from .protocols import SQLAlchemyProtocol, SQLAlchemyLiteProtocol
from .utilities import hook_base_model, get_app_ctx_id, apply_to_engines, clone_method

from .backends import fsa as _fsa
from .backends import fsa_lite as _fsa_lite
from .backends import is_module_invalid


P = ParamSpec("P")
T = TypeVar("T")
T2 = TypeVar("T2")
Ts = TypeVarTuple("Ts")

_SQLAlchemyDB = TypeVar("_SQLAlchemyDB", bound=SQLAlchemyProtocol)
_SQLAlchemyLiteDB_co = TypeVar(
    "_SQLAlchemyLiteDB_co", bound=SQLAlchemyLiteProtocol, covariant=True
)
_ModelLite_co = TypeVar("_ModelLite_co", bound=sa_orm.DeclarativeBase, covariant=True)

__all__ = ("SQLAlchemyProxy", "as_flask_sqlalchemy")


class SQLAlchemyProxy(Generic[_SQLAlchemyLiteDB_co, _ModelLite_co]):
    """Proxy class of `flask_sqlalchemy.SQLAlchemy`.

    This class is a wrapper of SQLAlchemy-Lite. By adjusting the behavior of the
    `flask_sqlalchemy_lite.SQLAlchemy`, it can mimic the usage of
    `flask_sqlalchemy.SQLAlchemy`.

    Note that not all the functionalities of `flask_sqlalchemy_lite.SQLAlchemy` can
    be exactly the same as the those of `flask_sqlalchemy.SQLAlchemy`. In specific,
    this proxy will do the following things:

    * Provide a `Model` based on the given argument `model_class`, where the
      `__tablename__` will be automatically inferred from `model_class`.
    * Provide a fake `Query` class. This `Query` class is just `sqlalchemy.orm.Query`.
      In other words, it does not provide any extra functionalities
    * Provide a fake `Table` class. This fake class is actually a method returning
      an `sqlalchemy.Table` instance, where users do not need to implement `metadata`.
    * Provide a scoped session like that of `flask_sqlalchemy.SQLAlchemy`. This scoped
      session is managed by this proxy class.
    * Provide other basic methods in `flask_sqlalchemy.SQLAlchemy`. The usages would
      be equivalent but the implmentation is based on `flask_sqlalchemy_lite`.
    * Any functionality that cannot be used will raise a `NotImplementedError`.

    This wrapper can be used when users need to migrate from Flask SQLAlchemy to
    Flask SQLAlchemy-Lite without making too many changes to the Object-Relationship-
    Mapping (ORM) codes. It is also useful if the users is primarily using Flask
    SQLAlchemy but want to support Flask SQLAlchemy Lite in some specific deployments.
    """

    def __init__(
        self, db: _SQLAlchemyLiteDB_co, model_class: Type[_ModelLite_co]
    ) -> None:
        """Initialzation.

        Arguments
        ---------
        db: `flask_sqlalchemy_lite.SQLAlchemy`
            The database instance exporting the session and engine instances.

            It is provided by the Flask extensions like `flask_sqlachemy_lite`. This
            wrapper will mimic the behaviors of `flask_sqlalchemy` even if the
            given instance is from the lite version.

        model_class: `type[DeclarativeBase]`
            The type of the base model. This `model_class` is mandatory.
            It needs to be used for providing the functionalities related to the
            metadata.
        """
        self.__db = db
        if isinstance(model_class, type) and issubclass(
            model_class, sa_orm.DeclarativeBase
        ):
            self.__model_class = hook_base_model(model_class, self.__db)
        else:
            raise TypeError(
                'flask_sqlalchemy_compat: The argument "model_class" {0} needs to '
                "be a subclass of DeclarativeBase which provides metadata."
            )
        self.__table_class = self._create_table(sa.Table)

        self.__metadatas: Dict[Optional[str], sa.MetaData] = {
            None: self.__model_class.metadata
        }
        self.__session: Optional[sa_orm.scoped_session[sa_orm.Session]] = None

    @property
    def db(self) -> _SQLAlchemyLiteDB_co:
        """Property: The `db` instance provided by the Flask SQLAlchemy extension."""
        return self.__db

    @property
    def Model(self) -> Type[_ModelLite_co]:
        """Property: The `Model` type. It can be used as the base class of the
        SQLAlchemy models. This value is `model_class` passed to the initialization
        of this wrapper.
        """
        return self.__model_class

    def _create_table(
        self, table_cls: Callable[Concatenate[str, sa.MetaData, P], sa.Table]
    ):
        """The factory used for creating a customized method that creates the
        `sa.Table` with the argument `metadata` implicitly set.
        """

        @overload
        def Table(name: str, *args: P.args, **kwargs: P.kwargs) -> sa.Table: ...

        @overload
        def Table(
            name: str, metadata: sa.MetaData, *args: P.args, **kwargs: P.kwargs
        ) -> sa.Table: ...

        @functools.wraps(sa.Table)
        def Table(name: str, *args: Any, **kwargs: Any) -> sa.Table:
            if len(args) > 0 and isinstance(args[0], sa.MetaData):
                return table_cls(name, *args, **kwargs)
            else:
                return table_cls(
                    name, self.__model_class.metadata, *cast(Any, args), **kwargs
                )

        return Table

    @property
    def Table(self):
        """A simplified version of `sa.Table`.

        Compared to `sa.Table`. The only difference is that the argument `metadata`
        has been implicitly configured. Users do not need to pass this argument when
        using this constructor.
        """
        return self.__table_class

    @property
    def Query(self) -> Type[sa_orm.Query]:
        """The same as `sa.orm.Query`."""
        return sa_orm.Query

    @property
    def session(self) -> sa_orm.scoped_session[sa_orm.Session]:
        """The same as `self.db.session`.

        The default session for the current application context. It will be
        closed when the context ends."""
        if self.__session is None:
            raise RuntimeError(
                'flask_sqlalchemy_compat: Need to run "init_app()" before using the '
                "session."
            )
        return self.__session

    @property
    def metadatas(self) -> Dict[Optional[str], sa.MetaData]:
        """The compatible interface of metadatas.

        Since `flask_sqlalchemy_lite` does not support `bind_key`, this `metdatas` is
        always implemented by a dictionary with only one member:
        ```python
        {None: self.metadata}
        ```
        """
        return self.__metadatas

    @property
    def metadata(self) -> sa.MetaData:
        """The default metadata used by `Model` and `Table` if no bind key is set."""
        return self.__model_class.metadata

    @property
    def engines(self) -> MutableMapping[Optional[str], sa_engine.Engine]:
        """The engines associated with the current application.

        To make this value compatible with `flask_sqlalchemy`. The returned value is
        added with an extra item: `self.engines[None] is self.engines["default"]`
        """
        default_dict: Dict[Optional[str], sa_engine.Engine] = {None: self.__db.engine}
        return collections.ChainMap(default_dict, cast(Any, self.__db.engines))

    @property
    def engine(self) -> sa_engine.Engine:
        """The engines associated with the current application."""
        return self.__db.engine

    def _teardown_session(self, exc: Optional[BaseException]) -> None:
        """Remove the current session at the end of the request.

        Add this method because this proxy class will add an extra session that
        the backend `self.db` does not provide.
        """
        self.session.remove()

    def __add_configs(self, app: flask.Flask) -> None:
        """Added configurations to the `app`.

        If the configurations have been configured for `flask_sqlalchemy_lite`, will
        attempt to convert the configurations to the format of `flask_sqlalchemy`.
        """
        if "SQLALCHEMY_ENGINES" in app.config:
            # Do nothing if the configuration is already ready for sqlalchemy
            return
        # Configurations of flask_sqlalchemy.
        engines_cfg: Dict[str, str] = dict()
        if "SQLALCHEMY_DATABASE_URI" in app.config:
            engines_cfg["default"] = app.config["SQLALCHEMY_DATABASE_URI"]
        if "SQLALCHEMY_BINDS" in app.config:
            fsa_binds = app.config["SQLALCHEMY_BINDS"]
            if isinstance(fsa_binds, collections.abc.Mapping):
                for key, val in fsa_binds.items():
                    if "default" in engines_cfg and key == "default":
                        continue
                    if isinstance(val, str):
                        engines_cfg[key] = val
                    if isinstance(val, collections.abc.Mapping) and "url" in val:
                        engines_cfg[key] = val["url"]
        if engines_cfg:
            app.config["SQLALCHEMY_ENGINES"] = engines_cfg

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
        self.__session = sa_orm.scoped_session(self.__db.sessionmaker, get_app_ctx_id)
        app.teardown_appcontext(self._teardown_session)

    def get_engine(
        self, bind_key: Optional[str] = None, **kwargs: Any
    ) -> sa_engine.Engine:
        """The same as `self.engines[bind_key]`

        Get the engine for the given bind key for the current application.
        This requires that a Flask application context is active.

        Arguments
        ---------
        bind_key: `str`
            The name of the engine.
        """
        if "bind" in kwargs:
            bind_key = kwargs.pop("bind")

        if bind_key is None:
            bind_key = "default"

        return self.__db.engines[bind_key]

    def get_or_404(
        self,
        entity: _EntityBindKey[T],
        ident: _PKIdentityArgument,
        *,
        description: Optional[str] = None,
        **kwargs: Any,
    ) -> T:
        """Like `session.get()` but aborts with a `404 Not Found` error instead of
        returning `None`.

        The usage is the same as `session.get()` except for the newly added argument
        `description`.

        Arguments
        ---------
        entity: `Model`
            The model class to query.

        ident: `Any | tuple[Any]`
            The primary key to query.

        description: `str | None`
            A custom message to show on the error page.

        **kwargs:
            Extra arguments passed to `session.get()`.

        Returns
        -------
        #1: `Model`
            The queried model entity.
        """
        value = self.session.get(entity, ident, **kwargs)

        if value is None:
            if description is None:
                description = "Could not find the value of: {0}.".format(entity)
            flask.abort(404, description=description)

        return value

    @overload
    def first_or_404(
        self, statement: sa.sql.Select[Tuple[T]], *, description: Optional[str] = None
    ) -> T: ...

    @overload
    def first_or_404(
        self,
        statement: sa.sql.Select["Tuple[T, T2, *Ts]"],
        *,
        description: Optional[str] = None,
    ) -> "Tuple[T, T2, *Ts]": ...

    def first_or_404(
        self, statement: sa.sql.Select[Any], *, description: Optional[str] = None
    ) -> Any:
        """Like `Result.scalar()`, but aborts with a `404 Not Found` error instead of
        returning `None`.

        Arguments
        ---------
        statement: `Select[Tuple[T, ...]]`
            The `select` statement to execute.

        description: `str | None`
            A custom message to show on the error page.

        Returns
        -------
        #1: `T, ...`
            The first returned results when the `statement` is found.
        """
        value = self.session.execute(statement).scalar()

        if value is None:
            flask.abort(404, description=description)

        return value

    @overload
    def one_or_404(
        self, statement: sa.sql.Select[Tuple[T]], *, description: Optional[str] = None
    ) -> T: ...

    @overload
    def one_or_404(
        self,
        statement: sa.sql.Select["Tuple[T, T2, *Ts]"],
        *,
        description: Optional[str] = None,
    ) -> "Tuple[T, T2, *Ts]": ...

    def one_or_404(
        self, statement: sa.sql.Select[Any], *, description: Optional[str] = None
    ) -> Any:
        """Like `Result.scalar_one()` but aborts with a `404 Not Found` error instead
        of raising `NoResultFound` or `MultipleResultsFound`.

        Arguments
        ---------
        statement: `Select[Tuple[T, ...]]`
            The `select` statement to execute.

        description: `str | None`
            A custom message to show on the error page.

        Returns
        -------
        #1: `T, ...`
            The first returned results when the `statement` is found.
        """
        try:
            return self.session.execute(statement).scalar_one()
        except (sa_exc.NoResultFound, sa_exc.MultipleResultsFound):
            flask.abort(404, description=description)

    def paginate(self, *args: Any, **kwargs: Any) -> Never:
        """This method is not implemented by the proxy."""
        raise NotImplementedError(
            "flask_sqlalchemy_compat: Method `paginate` is purely implemented in "
            "`flask_sqlalchemy`. It is not supported and will not be supported to "
            "call this method while using `flask_sqlalchemy_lite`."
        )

    def create_all(
        self, bind_key: Union[str, None, Sequence[Union[str, None]]] = "__all__"
    ) -> None:
        """Create tables that do not exist in the database by calling
        `metadata.create_all()` for all or some bind keys. This does not
        update existing tables, use a migration library for that.

        This requires that a Flask application context is active.

        Arguments
        ---------
        bind_key: `str | None | Sequence[str | None]`
            The name(s) of the engines where the metadata will be applied to.

            If using `__all__`, will apply the metadata to all defined engines.
        """
        apply_to_engines(
            self.__model_class.metadata.create_all,
            bind_key=bind_key,
            engines=self.__db.engines,
            default_engine=self.__db.engine,
        )

    def drop_all(
        self, bind_key: Union[str, None, Sequence[Union[str, None]]] = "__all__"
    ) -> None:
        """Drop tables by calling `metadata.drop_all()` for all or some bind keys.

        This requires that a Flask application context is active.

        Arguments
        ---------
        bind_key: `str | None | Sequence[str | None]`
            A bind key or list of keys of the engines to drop the tables from.

            If using `__all__`, will drop the tables from all defined engines.
        """
        apply_to_engines(
            self.__model_class.metadata.drop_all,
            bind_key=bind_key,
            engines=self.__db.engines,
            default_engine=self.__db.engine,
        )

    def reflect(
        self, bind_key: Union[str, None, Sequence[Union[str, None]]] = "__all__"
    ) -> None:
        """Load table definitions from the database by calling `metadata.reflect()`
        for all or some bind keys.

        This requires that a Flask application context is active.

        Arguments
        ---------
        bind_key: `str | None | Sequence[str | None]`
            A bind key or list of keys of the engines to reflect the tables from.

            If using `__all__`, will reflect the tables from all defined engines.
        """
        apply_to_engines(
            self.__model_class.metadata.reflect,
            bind_key=bind_key,
            engines=self.__db.engines,
            default_engine=self.__db.engine,
        )

    @clone_method(sa_orm.relationship)
    def relationship(self, *args: Any, **kwargs: Any):
        """The same as `sa_orm.relationship`"""
        return sa_orm.relationship(*args, **kwargs)

    @clone_method(sa_orm.dynamic_loader)
    def dynamic_loader(self, *args: Any, **kwargs: Any):
        """The same as `sa_orm.dynamic_loader`"""
        return sa_orm.dynamic_loader(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        if name == "relation":
            return sa_orm.relationship

        if name == "event":
            return sa_event

        if name.startswith("_"):
            raise AttributeError(name)

        for mod in (sa, sa_orm):
            if hasattr(mod, name):
                return getattr(mod, name)

        raise AttributeError(name)


@overload
def as_flask_sqlalchemy(db: _SQLAlchemyDB) -> _SQLAlchemyDB: ...


@overload
def as_flask_sqlalchemy(
    db: _SQLAlchemyLiteDB_co, model_class: Type[_ModelLite_co]
) -> SQLAlchemyProxy[_SQLAlchemyLiteDB_co, _ModelLite_co]: ...


def as_flask_sqlalchemy(
    db: Union[SQLAlchemyProtocol, SQLAlchemyLiteProtocol],
    model_class: Optional[Type[sa_orm.DeclarativeBase]] = None,
) -> Union[SQLAlchemyProxy[Any, Any], SQLAlchemyProtocol]:
    """Make `db` works as `flask_sqlalchemy`.

    Arguments
    ---------
    db: `flask_sqlalchemy.SQLAlchemy | flask_sqlalchemy_lite.SQLAlchemy`
        The db extension to be wrapped.

    model_class: `Type[sa_orm.DeclarativeBase] | None`
        The base model class used for mimicking the behavior of `db.Model` when
        `db` is not from `flask_sqlalchemy`. Note that this value will be modified
        inplace because some compatibility-related functionalities like auto table
        name and the query method need to be provided to make its usage aligned with
        `flask_sqlalchemy.SQLAlchemy().Model`.

        This value should not be used if `db` is provided by `flask_sqlalchemy`.

    Returns
    -------
    #1: `db: flask_sqlalchemy.SQLAlchemy`
        If `db` is already provided by `flask_sqlalchemy`, return as it is.

    #1: `SQLAlchemyProxy(db, model_class)`
        If `db` is provided by `flask_sqlalchemy_lite`, return a proxy wrapper of it.
        This wrapper has the same APIs of `flask_sqlalchemy.SQLAlchemy()` but
        the implementation is based on `flask_sqlalchemy_lite.SQLAlchemy()`.
    """
    if not is_module_invalid(_fsa):
        if isinstance(db, _fsa.SQLAlchemy):
            return db
    if not isinstance(model_class, type):
        raise TypeError(
            'flask_sqlalchemy_compat: The argument "model_class" is required because '
            'the argument "db" is not provided by `flask_sqlalchemy`.'
        )
    if not issubclass(model_class, sa_orm.DeclarativeBase):
        raise TypeError(
            'flask_sqlalchemy_compat: The argument "model_class" needs to be a '
            'subclass of "sa.orm.DeclarativeBase".'
        )
    if not is_module_invalid(_fsa_lite):
        if isinstance(db, _fsa_lite.SQLAlchemy):
            return SQLAlchemyProxy(db, model_class=model_class)
    raise TypeError(
        'flask_sqlalchemy_compat: Fail to convert "db" because of either of the '
        'following reasons: (1) Both "flask_sqlalchemy" and "flask_sqlalchemy_lite" '
        'are not installed. (2) "db" is not from "flask_sqlalchemy" or '
        '"flask_sqlalchemy_lite".'
    )
