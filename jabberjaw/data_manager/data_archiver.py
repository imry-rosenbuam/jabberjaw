import os
import logging
import polars as pl
import jabberjaw.utils.mkt_classes as mkt_classes
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class DataArchiver(ABC):
    """ template class for DataArchivers"""
    @classmethod
    @abstractmethod
    def load_mkt_data(cls, symbol_name: str) -> pl.DataFrame:
        """loads mkt data according to given symbol"""
        return pl.DataFrame()

    @classmethod
    @abstractmethod
    def save_mkt_data(cls, symbol_name: str, df: pl.DataFrame, msg: str = "") -> None:
        """ save data given a symbol"""
        raise Exception("save mkt data not implemented")


class DataArchiverArrow(DataArchiver):
    """Parquet implementation of DataArchiver"""
    @staticmethod
    def file_path(symbol_name):
        return mkt_classes.tsdb_path() + "data/" + symbol_name.upper() + ".arrow"

    @classmethod
    def save_mkt_data(cls, symbol_name: str, df: pl.DataFrame, msg: str = "") -> None:
        if not os.path.isdir(mkt_classes.tsdb_path() + "data"):
            os.mkdir(mkt_classes.tsdb_path() + "data")
        df.write_parquet(cls.file_path(symbol_name))
        logger.info(msg if msg else "Saved %s", symbol_name)

    @classmethod
    def load_mkt_data(cls, symbol_name: str) -> pl.DataFrame:
        if os.path.isfile(cls.file_path(symbol_name)):
            return pl.read_parquet(cls.file_path(symbol_name))
        return pl.DataFrame()


if __name__ == '__main__':
    to_load = 'IR_USD_COM-PAPER-F_3M@FRED'
    s = DataArchiverArrow.load_mkt_data(to_load)
    print(s)
