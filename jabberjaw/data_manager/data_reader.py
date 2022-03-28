import pandas_datareader as web
import pandas as pd
import datetime
from abc import ABC, abstractmethod


class DataReader(ABC):
    """ template class for DataReaders"""

    @classmethod
    @abstractmethod
    def download_data_eod(cls, ticker: str, source: str, start_date: datetime.datetime,
                          end_date: datetime.datetime) -> pd.DataFrame:
        raise Exception("Method not implemented")

    @classmethod
    @abstractmethod
    def download_data(cls, ticker: str):
        raise Exception("Method not implemented")


class DataReaderPD(DataReader):
    # download from source and convert it to the ref date and obs time schema
    # in our case the schema is banal as we only have eod data
    # we are using panda datareader in order to extract data
    @classmethod
    @abstractmethod
    def download_data_eod(cls, ticker: str, source: str, start_date: datetime.datetime,
                          end_date: datetime.datetime) -> pd.DataFrame:
        df = web.DataReader(ticker, source, start_date, end_date)
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)

        timestamps = list(df.index)
        obs_times = list(map(lambda x: x + pd.Timedelta('1 days') + pd.Timedelta('-1 sec'), timestamps))
        index = pd.MultiIndex.from_arrays([timestamps, obs_times], names=["Ref_Date", "Obs_Time"])

        return pd.DataFrame(index=index, data=df.values, columns=df.columns)


if __name__ == "__main__":
    # an example how to download data using the data reader, specifically with Pandas DataReader
    tck = "^FTSE"
    strt = datetime.datetime(year=2015, month=1, day=1)
    end = datetime.datetime(year=2022, month=12, day=31)
    src = 'yahoo'
    d = DataReaderPD.download_data_eod(tck, src, strt, end)
    print(d)
