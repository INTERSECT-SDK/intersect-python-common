"""Common definitions shared across ALL INTERSECT services, be they domain science microservices or INTERSECT core services.

You can use the base package as the public API, no need to import from submodules.

IMPORTANT: If you are building a scientific microservice, do NOT import from this package. Instead, import from intersect-sdk, which is the public-facing library intended for you. Relevant definitions from this package will be re-exported there.
"""

from importlib import import_module
from typing import TYPE_CHECKING

# import everything eagerly for IDEs/LSPs
if TYPE_CHECKING:
    from .config import (
        ControlPlaneConfig,
        ControlProvider,
        DataStoreConfig,
        DataStoreConfigMap,
        HierarchyConfig,
    )
    from .control_plane.control_plane_manager import ControlPlaneManager
    from .control_plane.definitions import MessageCallback
    from .core_definitions import IntersectDataHandler, IntersectMimeType
    from .data_plane.data_plane_manager import DataPlaneManager
    from .exceptions import IntersectApplicationError, IntersectError, IntersectSetupError
    from .version import __version__, intersect_sdk_version_info, intersect_sdk_version_string

__all__ = (
    'ControlPlaneConfig',
    'ControlPlaneManager',
    'ControlProvider',
    'DataPlaneManager',
    'DataStoreConfig',
    'DataStoreConfigMap',
    'HierarchyConfig',
    'IntersectApplicationError',
    'IntersectDataHandler',
    'IntersectError',
    'IntersectMimeType',
    'IntersectSetupError',
    'MessageCallback',
    '__version__',
    'intersect_sdk_version_info',
    'intersect_sdk_version_string',
)

# PEP 562 stuff: do lazy imports for people who just want to import from the top-level module

__lazy_imports = {
    'ControlPlaneConfig': '.config',
    'ControlProvider': '.config',
    'DataStoreConfig': '.config',
    'DataStoreConfigMap': '.config',
    'HierarchyConfig': '.config',
    'ControlPlaneManager': '.control_plane.control_plane_manager',
    'MessageCallback': '.control_plane.definitions',
    'IntersectDataHandler': '.core_definitions',
    'IntersectMimeType': '.core_definitions',
    'DataPlaneManager': '.data_plane.data_plane_manager',
    'IntersectApplicationError': '.exceptions',
    'IntersectError': '.exceptions',
    'IntersectSetupError': '.exceptions',
    '__version__': '.version',
    'intersect_sdk_version_info': '.version',
    'intersect_sdk_version_string': '.version',
}


def __getattr__(attr_name: str) -> object:
    attr_module = __lazy_imports.get(attr_name)
    if attr_module:
        module = import_module(attr_module, package=__spec__.parent)
        return getattr(module, attr_name)

    msg = f'module {__name__!r} has no attribute {attr_name!r}'
    raise AttributeError(msg)


def __dir__() -> list[str]:
    return list(__all__)
