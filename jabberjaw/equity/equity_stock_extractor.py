from ..mkt_utils import data_manager_parquet as dmp
from ..mkt_utils import mkt_classes as mkt_classes
import pandas as pd
import datetime

sources = ["default", "morningstar"]
default_source = "morningstar"


class EquityStockExtractor(mkt_classes.DataExtractor):
    @classmethod
    def load_mkt_data(cls, mkt_coord: mkt_classes.MktCoord, ref_data: datetime.date,
                      obs_time: datetime.datetime) -> dict:
        data = {}
        if mkt_coord.source in sources and mkt_coord.quote in ["default"]:
            mkt_coord_single_point = mkt_coord.copy()
            for k in mkt_coord.points:
                mkt_coord_single_point.points = tuple(k)
                data[k] = market_data_load(mkt_coord, ref_data, obs_time)
        else:
            raise Exception("Unknown source or quote style entered")

        return data


def market_data_load_yahoo(mkt_coord: mkt_classes.MktCoord, ref_date: datetime.date,
                           obs_time: datetime.datetime) -> dict:
    symbol: str = mkt_classes.mkt_symbol(mkt_coord)
    return dmp.get_data_point(symbol, ref_date, obs_time)


def market_data_load(mkt_coord: mkt_classes.MktCoord, ref_date: datetime.date, obs_time: datetime.datetime) -> dict:
    return dmp.get_data_point_mkt(mkt_coord, ref_date, obs_time)


def load_equity_cash_market_data(symbol: str, source: str = "DEFAULT") -> pd.DataFrame:
    mkt_c = mkt_classes.MktCoord('equity', 'stock', 'cash', (symbol,), source=source)
    mkt_symbol = mkt_c.mkt_symbol()
    df = dmp.market_data_load(mkt_symbol)
    return df


def mkt_coord_equity_coord(ticker: str, mkt_type: str, mkt_asset: str, source: str = None) -> mkt_classes.MktCoord:
    mkt_str: str = "_".join(["equity", mkt_type, mkt_asset, ticker])
    if source:
        mkt_str += '@' + source
    mkt_coord: mkt_classes.MktCoord = mkt_classes.parse_mkt_coord(mkt_str)
    return mkt_coord
