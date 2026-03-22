import datetime
import polars as pl
from jabberjaw.utils.mkt_classes import MktCoord
import jabberjaw.utils.mkt_classes as mkt_classes
from jabberjaw.data_manager.data_archiver import DataArchiver, DataArchiverArrow

data_archiver = DataArchiverArrow  # global variable to enable future changes


class DataLoader:
    data_archiver = data_archiver

    def __init_subclass__(cls, **kwargs):
        cls.data_archiver = data_archiver

    @classmethod
    def get_data_slice(cls, symbol_name: str, start_time: datetime.datetime, end_time: datetime.datetime,
                       return_dict: bool = True) -> pl.DataFrame:
        """load a slice of data for a symbol given a period (start_date,end_date) inclusive"""
        df = cls.data_archiver.load_mkt_data(symbol_name)
        return df.filter(
            (pl.col("REF_DATE") >= start_time) & (pl.col("REF_DATE") <= end_time)
        )

    @classmethod
    def get_data_ref_date(cls, symbol_name: str, ref_date: datetime.date) -> dict:
        """ loads EOD data for a refdate given a symbol to load"""
        ref_datetime = datetime.datetime.fromordinal(ref_date.toordinal())
        data_slice = cls.get_data_slice(symbol_name, ref_datetime, ref_datetime)
        if len(data_slice):
            return data_slice.row(-1, named=True)
        return {}

    @classmethod
    def get_data_point_obs_time(cls, symbol_name: str, ref_date: datetime.date, obs_time: datetime.datetime) -> dict:
        """loads data point given an observation time"""
        ref_datetime = datetime.datetime.fromordinal(ref_date.toordinal())
        data_slice = cls.get_data_slice(symbol_name, ref_datetime, ref_datetime).filter(
            pl.col("OBS_TIME") <= obs_time
        )
        if len(data_slice):
            return data_slice.row(-1, named=True)
        return {}

    @classmethod
    def get_data_point(cls, symbol_name: str, ref_date: datetime.date, obs_time: datetime.datetime = None) -> dict:
        """ loads data point given a symbol and a timestamp (refdate and optionally an observation time)"""
        if not obs_time:
            return cls.get_data_ref_date(symbol_name, ref_date)
        else:
            return cls.get_data_point_obs_time(symbol_name, ref_date, obs_time)

    @classmethod
    def get_data_point_mkt(cls, mkt_coord: mkt_classes.MktCoord, ref_date: datetime.date,
                           obs_time: datetime.datetime = None) -> dict:
        """ loads mkt data for a single date for a MktCoord"""
        symbol: str = mkt_coord.mkt_symbol()
        return cls.get_data_point(symbol, ref_date, obs_time)

    @classmethod
    def save_data(cls, mkt_coord: MktCoord, df: pl.DataFrame):
        """ save the data to the data directory"""
        symbol = mkt_coord.mkt_symbol()
        cls.data_archiver.save_mkt_data(symbol, df)

    @classmethod
    def load_mkt_data(cls, mkt_coord: MktCoord, ref_date: datetime.date, obs_time: datetime.datetime = None):
        """loads mkt data for a single refdate (capped by an observation time if provided)"""
        return cls.get_data_point_mkt(mkt_coord, ref_date, obs_time)

    @classmethod
    def load_mkt_data_history(cls, mkt_coord: MktCoord) -> pl.DataFrame:
        """loads the full time series of a MktCoord"""
        symbol_name = mkt_coord.mkt_symbol()
        return cls.data_archiver.load_mkt_data(symbol_name)
