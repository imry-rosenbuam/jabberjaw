from abc import ABC, abstractmethod
from jabberjaw.mkt_utils.mkt_classes import MktCoord, get_coord_default_source
from jabberjaw.data_manager import mkt_data_manager as dm
import datetime


class Marketiser(ABC):
    """ a class used as a template for the different asset marketisers"""

    @classmethod
    def marketise_mkt_point(cls, mkt_coord: MktCoord, start_date: datetime.date,
                            end_date: datetime.date, overwrite: bool = False) -> None:
        """ marketises a single MKtCoord according to given period ( start_date to end_date, inclusive)"""
        df = dm.get_history_mkt_data(mkt_coord)
        ticker, source = cls.get_ticker(mkt_coord)

        if not df.empty and not overwrite:
            print(ticker + " already MARKETISED")
            return None

        print("TRYING to Marketise " + ticker)
        df_new = dm.extract_data(ticker, source, datetime.datetime.fromordinal(start_date.toordinal()),
                                 datetime.datetime.fromordinal(end_date.toordinal()))
        if df.empty:
            df = df_new
        else:
            df.update(df_new)

        dm.save_mkt_data(mkt_coord, df)

    @classmethod
    def get_ticker(cls, mkt_coord: MktCoord) -> tuple:
        """ returns the ticker and source for a given MktCoord"""
        pt = mkt_coord.mkt_asset
        source = get_coord_default_source(mkt_coord) if mkt_coord.source in [None, "DEFAULT"] else mkt_coord.source
        return pt, source
