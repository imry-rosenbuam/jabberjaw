import yfinance as yf
from fredapi import Fred
import polars as pl
import datetime
import os
from datetime import timedelta
from abc import ABC, abstractmethod


sources = []


class DataReader(ABC):
    """template class for DataReaders"""

    @classmethod
    @abstractmethod
    def download_data_eod(cls, ticker: str, source: str, start_date: datetime.datetime,
                          end_date: datetime.datetime) -> pl.DataFrame:
        raise Exception("Method not implemented")

    @classmethod
    @abstractmethod
    def download_data(cls, ticker: str):
        raise Exception("Method not implemented")


def _build_polars_df(pd_df, date_col: str) -> pl.DataFrame:
    """Adds REF_DATE and OBS_TIME columns and converts to a polars DataFrame."""
    timestamps = list(pd_df[date_col])
    pd_df["REF_DATE"] = timestamps
    pd_df["OBS_TIME"] = [ts + timedelta(days=1) - timedelta(seconds=1) for ts in timestamps]
    pd_df.drop(columns=[date_col], inplace=True)
    return pl.from_pandas(pd_df)


class DataReaderYahoo(DataReader):
    """Downloads EOD data from Yahoo Finance via yfinance."""

    @classmethod
    def download_data_eod(cls, ticker: str, source: str = "yahoo",
                          start_date: datetime.datetime = None,
                          end_date: datetime.datetime = None) -> pl.DataFrame:
        pd_df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False, progress=False)
        pd_df.reset_index(inplace=True)
        # yfinance >= 0.2 returns MultiIndex columns for single tickers
        if hasattr(pd_df.columns, 'levels'):
            pd_df.columns = [col[0] for col in pd_df.columns]
        pd_df.columns = pd_df.columns.str.upper()
        return _build_polars_df(pd_df, "DATE")

    @classmethod
    def download_data(cls, ticker: str):
        raise Exception("Method not implemented")


class DataReaderFred(DataReader):
    """Downloads time series from FRED via fredapi."""

    @classmethod
    def download_data_eod(cls, ticker: str, source: str = "fred",
                          start_date: datetime.datetime = None,
                          end_date: datetime.datetime = None) -> pl.DataFrame:
        api_key = os.environ.get("FRED_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "FRED_API_KEY environment variable is not set. "
                "Get a free key at https://fred.stlouisfed.org/api/key"
            )
        fred = Fred(api_key=api_key)
        series = fred.get_series(ticker, observation_start=start_date, observation_end=end_date)
        pd_df = series.reset_index()
        pd_df.columns = ["DATE", ticker.upper()]
        return _build_polars_df(pd_df, "DATE")

    @classmethod
    def download_data(cls, ticker: str):
        raise Exception("Method not implemented")


if __name__ == "__main__":
    strt = datetime.datetime(year=2015, month=1, day=1)
    end = datetime.datetime(year=2021, month=12, day=31)
    print(DataReaderYahoo.download_data_eod("AAPL", start_date=strt, end_date=end))
    print(DataReaderFred.download_data_eod("DFF", start_date=strt, end_date=end))
