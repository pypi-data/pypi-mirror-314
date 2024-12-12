# -*- coding: UTF-8 -*-
"""
Flask SQLAlchemy Compat
=======================

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
Support the compatibility between `flask_sqlalchemy` and `flask_sqlalchemy_lite`.
It allows users to make minimal changes when they need to migrate from either one of
these two packages to each other.

The main motivation of this package is because `flask_sqlalchemy_lite` does not support
`python<=3.8`. This package is designed for providing the similar usages when users
have to make the `flask_sqlalchemy_lite` working with `python<=3.8` by using
`flask_sqlalchemy`. In this case, users can get rid of the difficulty of maintaining
two sets of codes.
"""

from pkgutil import extend_path

from . import backdict
from . import backends
from . import protocols
from . import utilities
from . import flask_sa_api
from . import flask_sa_lite_api
from . import auto

from .protocols import SQLAlchemyProtocol, SQLAlchemyLiteProtocol, ModelProtocol
from .utilities import TableNameGetter, QueryGetter
from .flask_sa_api import SQLAlchemyProxy, as_flask_sqlalchemy
from .flask_sa_lite_api import SQLAlchemyLiteProxy, as_flask_sqlalchemy_lite
from .auto import get_flask_sqlalchemy, get_flask_sqlalchemy_lite


__all__ = (
    "backdict",
    "backends",
    "protocols",
    "utilities",
    "flask_sa_api",
    "flask_sa_lite_api",
    "auto",
    "SQLAlchemyProtocol",
    "SQLAlchemyLiteProtocol",
    "ModelProtocol",
    "TableNameGetter",
    "QueryGetter",
    "SQLAlchemyProxy",
    "SQLAlchemyLiteProxy",
    "as_flask_sqlalchemy",
    "as_flask_sqlalchemy_lite",
    "get_flask_sqlalchemy",
    "get_flask_sqlalchemy_lite",
)

# Set this local module as the prefered one
__path__ = extend_path(__path__, __name__)

# Delete private sub-modules and objects
del extend_path
