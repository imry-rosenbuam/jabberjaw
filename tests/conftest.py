"""
Shared pytest fixtures.

TSDB_DATA must be set before any jabberjaw module is imported, so we do it
here at collection time via a module-level os.environ call, then override it
per-test with the tmp_path fixture where file I/O is needed.
"""
import os
import pytest

# Provide a default so the module-level env check in mkt_classes doesn't crash
# during collection. Individual tests that need a real path use the
# `tsdb_data_dir` fixture below.
os.environ.setdefault("TSDB_DATA", "/tmp/jabberjaw_test_data/")
os.environ.setdefault("FRED_API_KEY", "test_key")


@pytest.fixture
def tsdb_data_dir(tmp_path, monkeypatch):
    """Point TSDB_DATA at a temporary directory for the duration of a test."""
    data_dir = tmp_path / "tsdb"
    data_dir.mkdir()
    monkeypatch.setenv("TSDB_DATA", str(data_dir) + "/")
    return data_dir
