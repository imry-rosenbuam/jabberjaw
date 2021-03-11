from jabberjaw.data_manager.data_loader import DataLoader
from jabberjaw.mkt_utils import mkt_classes as mkt_classes
import datetime

sources = ["default", "morningstar"]


class EquityStockLoader(DataLoader):
    @classmethod
    def load_mkt_data(cls, mkt_coord: mkt_classes.MktCoord, ref_data: datetime.date,
                      obs_time: datetime.datetime) -> dict:
        """load mkt data for all points"""
        data = {}
        if mkt_coord.source in sources and mkt_coord.quote in ["default"]:
            mkt_coord_single_point = mkt_coord.copy()
            for k in mkt_coord.points:
                mkt_coord_single_point.points = tuple(k)
                data[k] = market_data_load(mkt_coord, ref_data, obs_time)
        else:
            raise Exception("Unknown source or quote style entered")

        return data


def market_data_load(mkt_coord: mkt_classes.MktCoord, ref_date: datetime.date, obs_time: datetime.datetime) -> dict:
    """ load the mkt data for a single point for a MktCoord with a single point"""
    return DataLoader.get_data_point_mkt(mkt_coord, ref_date, obs_time)

