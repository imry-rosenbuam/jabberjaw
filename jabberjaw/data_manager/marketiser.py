from abc import ABC, abstractmethod
from jabberjaw import utils
from jabberjaw.utils import mkt_classes
from jabberjaw.utils.mkt_classes import MktCoord, get_coord_default_source
from jabberjaw.data_manager import mkt_data_manager as dm
import datetime
import dpath.util as dp

class Marketiser(ABC):
    """ a class used as a template for the different asset marketisers"""

    mkt_type = None
    mkt_class = None
    
    
    @classmethod
    def mkt_class(cls) -> str:
        return ""
    
    @classmethod
    def mkt_type(cls) -> str:
        return ""
    
    @classmethod
    def marketise_ticker(cls, ticker:str,  source:str, start_date:datetime.date, end_date: datetime.date, overwrite: bool = False) -> None:
        mkt_coord = MktCoord(cls.mkt_class(),cls.mkt_type(),ticker,source=source)        
        cls.marketise_mkt_point(mkt_coord,start_date,end_date,overwrite)
    
    @classmethod
    def marketise_all_mkt_type_tickers(cls,start_date:datetime.date, end_date:datetime.date, overwrite: bool = False) -> None:
        """
        This function marketise all tickers for cash stocks
        :parm start_date: the date from which we marketise
        :parm end_date: the date will which we marketise (inclusive)
        :parm overwrite: a flag that determines if we overwrite existing data or not
        """
        cfg = mkt_classes.mkt_data_cfg()
        xpath = f'{cls.mkt_class()}/{cls.mkt_type()}'.upper()
        search= dp.search(cfg, xpath, yielded=True)
        tickers_to_marketise = [i for i in search].pop()[1]
        
        for ticker, metadata in tickers_to_marketise.items():
            cls.marketise_ticker(ticker, metadata['default_source'],start_date,end_date,overwrite)
        
        print('finished the marketisiation process for {}'.format(xpath))
    
    @classmethod
    def marketise_mkt_point(cls, mkt_coord: MktCoord, start_date: datetime.date,
                            end_date: datetime.date, overwrite: bool = False) -> None:
        """ marketises a single MKtCoord according to given period ( start_date to end_date, inclusive)"""
        points, tickers, source = cls.get_ticker(mkt_coord)


        
        tick_pnts = zip(tickers, points) if len(points) else [(tickers,tickers)]
        
        for ticker,pnt in tick_pnts:
            mkt_coord.point = pnt if len(points) else None
            df = dm.get_history_mkt_data(mkt_coord)
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
        pts = mkt_classes.get_points(mkt_coord)
        tickers = mkt_classes.get_ticker(mkt_coord)
        source = get_coord_default_source(mkt_coord) if mkt_coord.source in [None, "DEFAULT"] else mkt_coord.source
        return pts, tickers, source
