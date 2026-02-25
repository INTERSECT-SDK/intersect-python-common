"""Basic INTERSECT-SDK version information.

These values are often used programmatically by the SDK, but can be used by application developers as well.
"""

import re
from importlib.metadata import version


def _strip_version_metadata(version: str) -> str:
    """Given a string, do the following.

    1) Strip out pre-release/build-metadata from the string
    2) If the string is missing all of <MAJOR>.<MINOR>.<PATCH>, raise runtime error

    This is necessary because INTERSECT works off of a strict SemVer string and does not understand build metadata.
    """
    sem_ver = re.search(r'\d+\.\d+\.\d+', version)
    if sem_ver is None:
        msg = 'Package version does not contain a semantic version "<MAJOR>.<MINOR>.<DEBUG>", please fix this'
        raise RuntimeError(msg)
    return sem_ver.group()


# may include build metadata
__version__ = version('intersect-sdk-common')

intersect_sdk_version_string = _strip_version_metadata(__version__)
"""
Version string in the format <MAJOR>.<MINOR>.<DEBUG> . Follows semantic versioning rules, but ONLY in regard to the internal INTERSECT message/data structures. Strips out additional build metadata.
"""

intersect_sdk_version_info: tuple[int, int, int] = tuple(
    [int(x) for x in intersect_sdk_version_string.split('.')]
)  # type: ignore[assignment]
"""
Integer tuple in the format <MAJOR>,<MINOR>,<DEBUG> . Follows semantic versioning rules, but ONLY in regard to the internal INTERSECT message/data structures.
"""
