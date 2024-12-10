# -*- coding: UTF-8 -*-
"""
Backends
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
The backends of the `flask_sqlalchemy_compat` package. These backends are modules
conditionally loaded. In other words, if the model is intalled, will load the module.
Otherwise, load a placeholder of the corresponding module.

The backends include:
1. `fsa`: `flask_sqlalchemy`
    (licensed by BSD 3-Clause License, Copyright 2010 Pallets)
2. `fsa_lite`: `flask_sqlalchemy_lite`
    (licensed by MIT License, Copyright 2024 Pallets)
"""

import importlib
import importlib.util
from types import ModuleType
import sys

from typing import TYPE_CHECKING
from typing import Optional

try:
    from typing import Sequence
except ImportError:
    from collections.abc import Sequence

from typing_extensions import TypeGuard


__all__ = (
    "fsa",
    "fsa_lite",
    "ModulePlaceholder",
    "conditional_import",
    "is_module_invalid",
)


class ModulePlaceholder(ModuleType):
    """The placeholder module.

    This module is used as a placeholder of a module that cannot be found.
    It can still provide __name__ property. However, it does not contain
    the __spec__ property.
    """

    __file__: Optional[str] = None
    """The `file` attribute of this placeholder module is empty."""

    removed_kw = set(("__path__",))

    protected_kw = set(
        (
            "__repr__",
            "__str__",
            "__name__",
            "__qualname__",
            "__annotations__",
            "__spec__",
            "__origin__",
            "__weakref__",
            "__weakrefoffset__",
            "force_load",
            "__class__",
            "__dict__",
            "abstract",
        )
    )

    def __init__(self, name: str, doc: Optional[str] = None) -> None:
        """Initialization.
        Arguments:
            name: The module name. It will be passed to ModuleType.
        """
        name = str(name)
        if doc is None:
            doc = (
                "{0}\n"
                "This module is used as a placeholder, because the required "
                "module {0} is not found.".format(name)
            )
        else:
            doc = str(doc)
        super().__init__(name=name, doc=doc)

    def __repr__(self) -> str:
        """This repr is used for showing that this is a placeholder."""
        return "<ModulePlaceholder {name}>".format(
            name=object.__getattribute__(self, "__name__")
        )

    @property
    def __all__(self) -> Sequence[str]:
        """The attribute list of this placeholder module is empty."""
        return tuple()

    def force_load(self) -> None:
        """Nothing happens. Because this is a placeholder."""
        return

    def __getattribute__(self, attr: str):
        """Add more error information to the attribute error."""
        if attr in ModulePlaceholder.removed_kw:
            raise AttributeError(
                "{0} does not offer the attribute {1}".format("ModulePlaceholder", attr)
            )
        if attr in ModulePlaceholder.protected_kw:
            try:
                return object.__getattribute__(self, attr)
            except AttributeError:
                pass
        try:
            return super().__getattribute__(attr)
        except AttributeError as err:
            name = object.__getattribute__(self, "__name__")
            raise ImportError(
                'utils: Fail to fetch the attribute "{0}" from module "{1}" '
                "because this optional module is not successfully loaded. At least "
                "one dependency of this module is not installed.".format(attr, name)
            ) from err


def conditional_import(name: str) -> ModuleType:
    """Import the module if it exists. Otherwise, return a `ModulePlaceholder`."""
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.find_spec(name)
    if spec is None:
        return ModulePlaceholder(name)
    if spec.loader is None:
        return ModulePlaceholder(name)
    # module = importlib.import_module(name)
    # return module
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def is_module_invalid(module: ModuleType) -> TypeGuard[ModulePlaceholder]:
    """Check whether the given module is invalid or not.

    An invalid module does not provide any functionalities but only serves as a
    placeholder.
    """
    return isinstance(module, ModulePlaceholder)


# Import sub-modules
if TYPE_CHECKING:
    import flask_sqlalchemy as fsa
    import flask_sqlalchemy_lite as fsa_lite
else:
    # Create conditional-loaded modules.
    fsa = conditional_import("flask_sqlalchemy")
    fsa_lite = conditional_import("flask_sqlalchemy_lite")
