"""Tests for jabberjaw.data_manager.data_loader"""
import datetime
import polars as pl
import pytest
from unittest.mock import MagicMock, patch
from jabberjaw.data_manager.data_loader import DataLoader
from jabberjaw.utils.mkt_classes import MktCoord


def _make_df(*ref_dates: datetime.datetime) -> pl.DataFrame:
    """Helper to build a minimal market data DataFrame."""
    return pl.DataFrame({
        "REF_DATE": list(ref_dates),
        "OBS_TIME": [d + datetime.timedelta(hours=23, seconds=59) for d in ref_dates],
        "VALUE": [float(i + 1) for i in range(len(ref_dates))],
    })


@pytest.fixture
def mock_archiver():
    archiver = MagicMock()
    archiver.load_mkt_data.return_value = _make_df(
        datetime.datetime(2022, 1, 3),
        datetime.datetime(2022, 1, 4),
        datetime.datetime(2022, 1, 5),
    )
    return archiver


class TestGetDataSlice:
    def test_filters_by_date_range(self, mock_archiver):
        DataLoader.data_archiver = mock_archiver
        result = DataLoader.get_data_slice(
            "SYM",
            datetime.datetime(2022, 1, 4),
            datetime.datetime(2022, 1, 4),
        )
        assert len(result) == 1
        assert result["VALUE"][0] == 2.0

    def test_returns_empty_for_out_of_range(self, mock_archiver):
        DataLoader.data_archiver = mock_archiver
        result = DataLoader.get_data_slice(
            "SYM",
            datetime.datetime(2023, 1, 1),
            datetime.datetime(2023, 1, 1),
        )
        assert result.is_empty()


class TestGetDataRefDate:
    def test_returns_last_row_as_dict(self, mock_archiver):
        DataLoader.data_archiver = mock_archiver
        result = DataLoader.get_data_ref_date("SYM", datetime.date(2022, 1, 3))
        assert isinstance(result, dict)
        assert result["VALUE"] == 1.0

    def test_returns_empty_dict_when_no_data(self, mock_archiver):
        mock_archiver.load_mkt_data.return_value = pl.DataFrame({
            "REF_DATE": [], "OBS_TIME": [], "VALUE": []
        })
        DataLoader.data_archiver = mock_archiver
        result = DataLoader.get_data_ref_date("SYM", datetime.date(2022, 1, 3))
        assert result == {}
