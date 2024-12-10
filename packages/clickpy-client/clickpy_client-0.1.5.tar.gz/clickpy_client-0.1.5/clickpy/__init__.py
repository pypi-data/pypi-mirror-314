from importlib import metadata as _metadata

from clickpy.client import ClickPyClient  # noqa: F401

try:
    __version__ = _metadata.version('clickpy-client')

except _metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = '0.0.0'
