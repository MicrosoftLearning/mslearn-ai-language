"""Real-Time Voice package root.

Reintroduced to allow hatchling to detect the package under src/ for building wheels/editable installs.
"""
from importlib.metadata import version, PackageNotFoundError

try:  # pragma: no cover - simple metadata fetch
    __version__ = version("real-time-voice")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+dev"

__all__ = ["__version__"]
