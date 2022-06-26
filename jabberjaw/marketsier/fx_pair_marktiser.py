import datetime
import dpath.util as dp
from jabberjaw.utils import mkt_classes
from jabberjaw.data_manager.marketiser import Marketiser

class FXSpotMarketiser(Marketiser):
    @classmethod
    def mkt_class(cls) -> str:
        return "fx".upper()

    @classmethod
    def mkt_type(cls) -> str:
        return "currency pair".upper()
    
    @classmethod
    def marketise_fx_spot_pair(cls,ccy_pair:str,source:str,start_date:datetime.date, end_date:datetime.date,overwrite:bool = False) -> None:
        mkt_c = mkt_classes.MktCoord('fx','currency pair', ccy_pair,source=source)
        cls.marketise_mkt_point(mkt_c,start_date,end_date,overwrite=overwrite)

    @classmethod
    def marketise_fx_spot_all_pairs(cls,start_date:datetime.date,end_date:datetime.date,overwrite:bool=False) -> None:
        mkt_cfg = mkt_classes.mkt_data_cfg()
        xpath = f'fx/currency pair'.upper()
        search = dp.search(mkt_cfg,xpath,yielded=True)
        fx_spots = [i for i in search].pop()[1]

        for ticker, metadata in fx_spots.items():
            try:
                cls.marketise_fx_spot_pair(ticker,metadata['default_source'],start_date,end_date,overwrite)
            except:
                print(f"failed to marketise {ticker}")
                
if __name__ == "__main__":
    ccy = "usdeur"
    start = datetime.date(year=2020, month=1, day=1)
    end = datetime.date.today()
    #FXSpotMarketiser.marketise_fx_spot_pair(ccy,'yahoo',start,end,overwrite=True)
    FXSpotMarketiser.marketise_fx_spot_all_pairs(start,end,overwrite=True)
    print('le fin')