# -*- coding: UTF-8 -*-
"""
Protocols
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
The customized protocol type hints used by this package. These protocols can be used
to notate the extension like `flask_sqlalchemy.SQLAlchemy` or the customized class
`flask_sqlalchemy.model.Model` without actually importing the package.
"""

from typing import Optional, Any
from typing import TYPE_CHECKING

try:
    from typing import Mapping, Callable
    from typing import Dict, Type
except ImportError:
    from collections.abc import Mapping, Callable
    from builtins import dict as Dict, type as Type

from typing_extensions import ClassVar, Protocol

import sqlalchemy as sa
import sqlalchemy.ext.asyncio as sa_async
import sqlalchemy.orm as sa_orm
from flask import Flask

if TYPE_CHECKING:
    from flask.sansio.app import App
else:  # Compatibility with Flask>=2,<3
    try:
        from flask.sansio.app import App
    except ImportError:
        from flask import Flask as App


__all__ = (
    "ModelProtocol",
    "SQLAlchemySharedProtocol",
    "SQLAlchemyLiteProtocol",
    "SQLAlchemyProtocol",
)


class ModelProtocol(Protocol):
    """Protocol compatible with `flask_sqlalchemy.extensions._FSAModel`.

    This protocol contains the general functionality of the model prototype. Flask
    SQLAlchemy does not use the native SQLAlchemy model but defines its own version.
    That's why we need this protocol for the compatibility issue.

    Note that this protocol does not cover every functionality of the Flask SQLAlchemy
    model for the compaiblity of a regular base model from SQLAlchemy.
    """

    query_class: ClassVar[Type[Any]]
    """Query class used by `query`. Defaults to `flask_sqlalchemy.SQLAlchemy.Query`."""

    query: ClassVar[Any]
    """A SQLAlchemy query for a model. Equivalent to `db.session.query(Model)`. Can
    be customized per-model by overriding `query_class`."""

    @property
    def metadata(self) -> sa.MetaData:
        """Metadata property synthesized by the `flask_sqlalchemy.SQLAlchemy` instance."""
        ...


class SQLAlchemySharedProtocol(Protocol):
    """Protocol compatible with both Flask SQLAlchemy and Flask SQLAlchemy Lite.

    This protocol only implments limited functionalies that are provided by both
    `flask_sqlalchemy.SQLAlchemy` and `flask_sqlalchemy_lite.SQLAlchemy`.
    Since this procol has the minimal coverage, it can be used for generalized
    purposes.
    """

    @property
    def engine(self) -> sa.Engine:
        """The default engine associated with the current application."""
        ...


class SQLAlchemyLiteProtocol(SQLAlchemySharedProtocol, Protocol):
    """Protocol compatible with Flask SQLAlchemy Lite.

    Flask SQLAlchemy Lite provides less functionality compared to Flask SQlAlchemy.
    It is ready since `Python>=3.9`. Although this package is new, it is still
    preferred because it works better with `SQLAlchemy>=2` and Python's `typing`
    system.

    This protocol covers most but does not include all functionalities of
    `flask_sqlalchemy_lite.SQLAlchemy`.
    """

    def init_app(self, app: App) -> None:
        """Register the extension on an application, creating engines from its
        `Flask.config`.
        """
        ...

    @property
    def engines(self) -> Dict[str, sa.Engine]:
        """The engines associated with the current application."""
        ...

    @property
    def sessionmaker(self) -> sa_orm.sessionmaker[sa_orm.Session]:
        """The session factory configured for the current application. This can
        be used to create sessions directly, but they will not be closed
        automatically at the end of the application context. Use `session`
        and `get_session` for that."""
        ...

    @property
    def session(self) -> sa_orm.Session:
        """The default session for the current application context. It will be
        closed when the context ends.
        """
        ...

    @property
    def async_engines(self) -> Dict[str, sa_async.AsyncEngine]:
        """The async engines associated with the current application."""
        ...

    @property
    def async_engine(self) -> sa_async.AsyncEngine:
        """The default async engine associated with the current application."""
        ...

    @property
    def async_sessionmaker(self) -> sa_async.async_sessionmaker[sa_async.AsyncSession]:
        """The async session factory configured for the current application."""
        ...

    @property
    def async_session(self) -> sa_async.AsyncSession:
        """The default async session for the current application context. It
        will be closed when the context ends.
        """
        ...


class SQLAlchemyProtocol(SQLAlchemySharedProtocol, Protocol):
    """Protocol compatible with Flask SQLAlchemy.

    Flask SQLAlchemy has been maintained for many years. It has a big community and
    many users, granting many available plugins that have served various applications
    for long. However, it works better with `SQLAlchemy<2`. For the new SQLAlchemy
    package heavily dependent on the modern typing system, this old extension pacakge
    may have several unsolved compatibility issues.

    Note that users still have to use it if they are working with `Python<3.9` because
    Flask SQLAlchemy Lite is not available for the legacy Python versions.

    This protocol covers most but does not include all functionalities of
    `flask_sqlalchemy.SQLAlchemy`.
    """

    def init_app(self, app: Flask) -> None:
        """Initialize a Flask application for use with this extension instance. This
        must be called before accessing the database engine or session with the app.
        """
        ...

    @property
    def engines(self) -> Mapping[Optional[str], sa.Engine]:
        """Map of bind keys to `sqlalchemy.engine.Engine` instances for current
        application. The `None` key refers to the default engine."""
        ...

    @property
    def session(self) -> sa_orm.scoped_session[Any]:
        """The default session for the current application context. It will be
        closed when the context ends.
        """
        ...

    @property
    def metadatas(self) -> Mapping[Optional[str], sa.MetaData]:
        """Map of bind keys to `sqlalchemy.schema.MetaData` instances. The `None` key
        refers to the default metadata.
        """
        ...

    @property
    def metadata(self) -> sa.MetaData:
        """The default metadata used by `Model` and `Table` if no bind key is set."""
        ...

    @property
    def Query(self) -> Callable[..., sa_orm.Query]:
        """The default query class used by `Model.query` and `lazy="dynamic"`
        relationships."""
        ...

    @property
    def Table(self) -> Callable[..., sa.Table]:
        """The default query class used by `Model.query` and `lazy="dynamic"`
        relationships."""
        ...

    @property
    def Model(self) -> Callable[..., ModelProtocol]:
        """The default query class used by `Model.query` and `lazy="dynamic"`
        relationships."""
        ...
