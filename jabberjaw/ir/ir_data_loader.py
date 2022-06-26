from jabberjaw.data_manager.data_loader import DataLoader
from jabberjaw.utils import mkt_classes
import datetime

sources = ["morningstar","default"]

class IRDataLoader(DataLoader):
    @classmethod
    def load_ir_point_mkt_data(cls, ticker:str,mkt_type:str, point:str,ref_date: datetime.date, obs_time: datetime.datetime = None):
        mc = mkt_classes.parse_mkt_coord("ir_"+mkt_type+"_"+ticker+"_" + point)
        return super().load_mkt_data(mc, ref_date, obs_time=obs_time)

    @classmethod
    def load_ir_point_mkt_data_history(cls, ticker:str, mkt_type:str, point: str):
        mc = mkt_classes.parse_mkt_coord("ir_"+mkt_type+"_"+ticker+ "_" + point)
        return super().load_mkt_data_history(mc)

if __name__ == "__main__":
    dt = datetime.date(year=2020, month=11, day=17)
    #bla = FXDataLoader.load_fx_spot_mkt_data("usdeur", "currency pair", dt)
    bla2 = IRDataLoader.load_ir_point_mkt_data_history("T-BILL","usd", "4WK")
    print(bla2)
    
    
    print("Le Fin")