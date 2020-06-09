import pyarrow.parquet as pq
import pandas as pd
import mkt_utils.mkt_classes as mkt_classes
import os
import datetime


def file_path(symbol_name):
    return mkt_classes.tsdb_path() + symbol_name.upper() + ".parquet"


def market_data_save(symbol_name: str, df: pd.DataFrame, msg: str = "") -> None:
    df.to_parquet(file_path(symbol_name))
    if msg == "":
        print("markeitsed to " + symbol_name)
    else:
        print(msg)


def market_data_load(symbol_name: str) -> pd.DataFrame:
    if os.path.isfile(file_path(symbol_name)):
        df = pd.read_parquet(file_path(symbol_name))
        return df

    return pd.DataFrame()


# return a slice of data according to ref date
def get_data_slice(symbol_name: str, start_time: datetime.datetime, end_time: datetime.datetime,
                   return_dict: bool = True):
    df = market_data_load(symbol_name)
    return df[pd.Timestamp(start_time):pd.Timestamp(end_time)]



def get_data_ref_date(symbol_name: str, ref_date: datetime.date) -> dict:
    ref_datetime = datetime.datetime.fromordinal(ref_date.toordinal())
    data_slice = get_data_slice(symbol_name, ref_datetime, ref_datetime)
    if len(data_slice):
        return data_slice.iloc[-1].to_dict()
    else:
        return data_slice


# TODO: check veracity of the call
def get_data_point_obs_time(symbol_name: str, ref_date: datetime.date, obs_time: datetime.datetime) -> dict:
    ref_datetime = datetime.datetime.fromordinal(ref_date.toordinal())
    data_slice = get_data_slice(symbol_name, ref_datetime, ref_datetime)[pd.Timestamp(ref_datetime):(pd.Timestamp(ref_datetime),
                                                  pd.Timestamp(obs_time))]

    if len(data_slice):
        return data_slice[-1].to_dict()
    else:
        return data_slice.to_dict()


def get_data_point(symbol_name: str, ref_date: datetime.date, obs_time: datetime.datetime = None) -> dict:
    if not obs_time:
        return get_data_ref_date(symbol_name, ref_date)
    else:
        return get_data_point_obs_time(symbol_name, ref_date, obs_time)
