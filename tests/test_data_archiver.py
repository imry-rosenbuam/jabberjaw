"""Tests for jabberjaw.data_manager.data_archiver"""
import polars as pl
import pytest
from unittest.mock import patch


class TestDataArchiverArrow:
    def test_save_and_load_roundtrip(self, tsdb_data_dir):
        from jabberjaw.data_manager.data_archiver import DataArchiverArrow

        symbol = "TEST_SYMBOL"
        df = pl.DataFrame({"REF_DATE": ["2021-01-01"], "VALUE": [1.23]})

        with patch("jabberjaw.utils.mkt_classes.tsdb_path", return_value=str(tsdb_data_dir) + "/"):
            (tsdb_data_dir / "data").mkdir()
            DataArchiverArrow.save_mkt_data(symbol, df)
            result = DataArchiverArrow.load_mkt_data(symbol)

        assert result.shape == df.shape
        assert result["VALUE"][0] == pytest.approx(1.23)

    def test_load_missing_symbol_returns_empty(self, tsdb_data_dir):
        from jabberjaw.data_manager.data_archiver import DataArchiverArrow

        with patch("jabberjaw.utils.mkt_classes.tsdb_path", return_value=str(tsdb_data_dir) + "/"):
            result = DataArchiverArrow.load_mkt_data("NONEXISTENT_SYMBOL")

        assert result.is_empty()

    def test_save_creates_data_directory(self, tsdb_data_dir):
        from jabberjaw.data_manager.data_archiver import DataArchiverArrow

        df = pl.DataFrame({"VALUE": [42.0]})
        with patch("jabberjaw.utils.mkt_classes.tsdb_path", return_value=str(tsdb_data_dir) + "/"):
            DataArchiverArrow.save_mkt_data("NEWDIR_TEST", df)
            assert (tsdb_data_dir / "data").exists()
