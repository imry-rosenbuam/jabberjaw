import os
import pandas as pd
import jabberjaw.mkt_utils.mkt_classes as mkt_classes
from abc import ABC, abstractmethod


class DataArchiver(ABC):
    """ template class for DataArchivers"""
    @classmethod
    @abstractmethod
    def load_mkt_data(cls, symbol_name: str) -> pd.DataFrame:
        """loads mkt data according to given symbol"""
        return pd.DataFrame()

    @classmethod
    @abstractmethod
    def save_mkt_data(cls, symbol_name: str, df: pd.DataFrame, msg: str = "") -> None:
        """ save data given a symbol"""
        raise Exception("save mkt data not implemented")


class DataArchiverParquet(DataArchiver):
    """Parquet implementation of DataArchiver"""
    @staticmethod
    def file_path(symbol_name):
        return mkt_classes.tsdb_path() + "data/" + symbol_name.upper() + ".parquet"

    @classmethod
    # parquet is not working for py 3.9
    def save_mkt_data(cls, symbol_name: str, df: pd.DataFrame, msg: str = "") -> None:
        # df.to_parquet(file_path(symbol_name)) for now we use HDF instead of parquet as it is not available for py 3.9
        if not os.path.isdir(mkt_classes.tsdb_path() + "data"):
            os.mkdir(mkt_classes.tsdb_path() + "data")

        df.to_hdf(cls.file_path(symbol_name), 'df')
        if msg == "":
            print("marketised to " + symbol_name)
        else:
            print(msg)

    @classmethod
    def load_mkt_data(cls, symbol_name: str) -> pd.DataFrame:
        if os.path.isfile(cls.file_path(symbol_name)):
            # df = pd.read_parquet(file_path(symbol_name)) for now we use HDF instead of parquet as it is not
            # available for py 3.9
            df: pd.DataFrame = pd.read_hdf(cls.file_path(symbol_name), 'df')
            return df

        return pd.DataFrame()



if __name__ == '__main__':
    to_load = 'EQUITY_SINGLE STOCK_NOV@YAHOO'
    s = DataArchiverParquet.load_mkt_data(to_load)
    xx = 1
