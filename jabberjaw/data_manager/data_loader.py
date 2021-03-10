import datetime
from jabberjaw.mkt_utils.mkt_classes import MktCoord
import jabberjaw.mkt_utils.mkt_classes as mkt_classes
import pandas as pd
from jabberjaw.data_manager.data_archiver import DataArchiver, DataArchiverParquet

data_archiver = DataArchiverParquet  # let us use this variable as global variable to enable future changes


class DataLoader:
    data_archiver = data_archiver

    def __init_subclass__(cls, **kwargs):
        cls.data_archiver = data_archiver

    @classmethod
    # return a slice of data according to ref date
    def get_data_slice(cls, symbol_name: str, start_time: datetime.datetime, end_time: datetime.datetime,
                       return_dict: bool = True):
        df = cls.data_archiver.load_mkt_data(symbol_name)
        return df[pd.Timestamp(start_time):pd.Timestamp(end_time)]

    @classmethod
    def get_data_ref_date(cls, symbol_name: str, ref_date: datetime.date) -> dict:
        ref_datetime = datetime.datetime.fromordinal(ref_date.toordinal())
        data_slice = cls.get_data_slice(symbol_name, ref_datetime, ref_datetime)
        if len(data_slice):
            return data_slice.iloc[-1].to_dict()
        else:
            return data_slice

    # TODO: check veracity of the call
    @classmethod
    def get_data_point_obs_time(cls, symbol_name: str, ref_date: datetime.date, obs_time: datetime.datetime) -> dict:
        ref_datetime = datetime.datetime.fromordinal(ref_date.toordinal())
        data_slice = cls.get_data_slice(symbol_name, ref_datetime, ref_datetime)[
                     pd.Timestamp(ref_datetime):(pd.Timestamp(ref_datetime),
                                                 pd.Timestamp(obs_time))]

        if len(data_slice):
            return data_slice[-1].to_dict()
        else:
            return data_slice.to_dict()

    @classmethod
    def get_data_point(cls, symbol_name: str, ref_date: datetime.date, obs_time: datetime.datetime = None) -> dict:
        if not obs_time:
            return cls.get_data_ref_date(symbol_name, ref_date)
        else:
            return cls.get_data_point_obs_time(symbol_name, ref_date, obs_time)

    @classmethod
    def get_data_point_mkt(cls, mkt_coord: mkt_classes.MktCoord, ref_date: datetime.date,
                           obs_time: datetime.datetime = None) -> dict:
        symbol: str = mkt_coord.mkt_symbol(mkt_coord)
        return cls.get_data_point(symbol, ref_date, obs_time)

    @classmethod
    def save_data(cls, mkt_coord: MktCoord, df: pd.DataFrame):
        symbol = mkt_coord.mkt_symbol()
        cls.data_archiver.save_mkt_data(symbol, df)

    @classmethod
    def load_mkt_data(cls, mkt_coord: MktCoord, ref_date: datetime.date, obs_time: datetime.datetime = None):
        return cls.get_data_point_mkt(mkt_coord, ref_date, obs_time)

    @classmethod
    def load_mkt_data_history(cls, mkt_coord):
        symbol_name = mkt_coord.mkt_symbol()
        return cls.data_archiver.load_mkt_data(symbol_name)
