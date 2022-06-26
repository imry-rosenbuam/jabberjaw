import datetime
import dpath.util as dp
from jabberjaw.utils import mkt_classes
from jabberjaw.data_manager.marketiser import Marketiser
import time

class IRUSDMarketiser(Marketiser):
    @classmethod
    def mkt_class(cls) -> str:
        return "ir".upper()
    
    @classmethod
    def mkt_type(cls) -> str:
        return "usd".upper()
    
    @classmethod
    def marketise_ir_usd_point(cls, point: str, source: str, start_date: datetime.date, end_date: datetime.date, overwrite:bool = False) -> None:
        
        mkt_c = mkt_classes.MktCoord("ir", "usd", point, source=source)
        cls.marketise_mkt_point(mkt_c,start_date,end_date,overwrite=overwrite)
        
    @classmethod
    def marketise_ir_all_ccy_points(cls,start_date:datetime.date,end_date:datetime.date,overwrite:bool=False) -> None:
        mkt_cfg = mkt_classes.mkt_data_cfg()
        xpath = f'ir/usd'.upper()
        search = dp.search(mkt_cfg,xpath,yielded=True)
        ir_points = [i for i in search].pop()[1]

        for point, metadata in ir_points.items():
            try:
                cls.marketise_ir_usd_point(point,metadata['default_source'],start_date,end_date,overwrite)
            except:
                print(f"failed to marketise {point}")
                
                
if __name__ == "__main__":
    start = datetime.date(year=2000, month=1, day=1)
    end = datetime.date.today()
    IRUSDMarketiser.marketise_ir_all_ccy_points(start,end,overwrite=True)
    #IRUSDMarketiser.marketise_ir_usd_point("T-BILL","FRED",start,end,overwrite=True)
    print("le fin")