import importlib
import importlib.metadata

from pytest import MonkeyPatch

import projgeom


def test_version_fallback(monkeypatch: MonkeyPatch) -> None:
    """__init__ reports 'unknown' when the distribution is missing (lines 18-19)."""

    def fake_version(name: str) -> str:
        raise importlib.metadata.PackageNotFoundError(name)

    with monkeypatch.context() as m:
        m.setattr(importlib.metadata, "version", fake_version)
        importlib.reload(projgeom)
        assert projgeom.__version__ == "unknown"

    importlib.reload(projgeom)
    assert projgeom.__version__ != "unknown"


def test_version_reported() -> None:
    """Installed distribution yields a non-empty version string."""
    assert projgeom.__version__ != ""
