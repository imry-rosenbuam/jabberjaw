import mkt_utils.data_manager_parquet as dmp
import mkt_utils.mkt_classes as mkt_classes
import datetime


class EquityIndexExtractor(mkt_classes.DataExtractor):
    @classmethod
    def load_mkt_data(cls, mkt_coord: mkt_classes.MktCoord, ref_data: datetime.date,
                      obs_time: datetime.datetime) -> dict:
        if mkt_coord.source in ["default", "yahoo"] and mkt_coord.quote in ["default"]:
            dp = market_data_load_yahoo(mkt_coord, ref_data, obs_time)
        else:
            raise Exception("Unknown source or quote style entered")

        return {"spot": dp}


def market_data_load_yahoo(mkt_coord: mkt_classes.MktCoord, ref_date: datetime.date,
                           obs_time: datetime.datetime) -> dict:
    return dmp.get_data_point(mkt_coord.category, ref_date, obs_time)
