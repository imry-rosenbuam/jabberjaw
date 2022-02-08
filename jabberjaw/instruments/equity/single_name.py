import  pandas as pd
import numpy as np
from jabberjaw.utils.instrument import Instrument, instrument
from dataclasses import dataclass, field
from jabberjaw.utils.mkt_classes import MktCoord
from jabberjaw.utils.mkt import Mkt
from dataclasses import dataclass
import datetime
@instrument
class SingleNameEquity(Instrument):
    single_name: str = None
    
    def __post_init__(self):
        if not self.single_name:
            raise "No Single name was inputed"
        self.mkt_coord=MktCoord('equity','single stock', self.single_name)
        
    def price(self) -> float:
        
       if self.mkt_coord.mkt_class == 'EQUITY' and self.mkt_coord.mkt_type == 'SINGLE STOCK':
            return self.mkt.get_mkt_data(self.mkt_coord)
       else:
           raise "Unkown Mkt Coordinate"    
       
if __name__ == "__main__":
    dt = datetime.date(year=2020, month=11, day=16)
    mkt = Mkt(ref_date=dt)
    
    bla = SingleNameEquity(mkt=mkt,ccy="USD",single_name="AAPL") 
    print(bla.price())
    print('Le fin')
