from ..mkt_utils import data_manager_parquet as dmp
from ..mkt_utils import mkt_classes as mkt_classes

import datetime

sources = ["default", "yahoo"]
default_source = "yahoo"


class EquityIndexExtractor(mkt_classes.DataExtractor):
    @classmethod
    def load_mkt_data(cls, mkt_coord: mkt_classes.MktCoord, ref_data: datetime.date,
                      obs_time: datetime.datetime) -> dict:
        if mkt_coord.source in sources and mkt_coord.quote in ["default"]:
            dp = market_data_load(mkt_coord, ref_data, obs_time)
        else:
            raise Exception("Unknown source or quote style entered")

        return {"spot": dp}


def market_data_load_yahoo(mkt_coord: mkt_classes.MktCoord, ref_date: datetime.date,
                           obs_time: datetime.datetime) -> dict:
    symbol: str = mkt_classes.mkt_symbol(mkt_coord)
    return dmp.get_data_point(symbol, ref_date, obs_time)


def market_data_load(mkt_coord: mkt_classes.MktCoord, ref_date: datetime.date, obs_time: datetime.datetime) -> dict:
    return dmp.get_data_point_mkt(mkt_coord, ref_date, obs_time)
