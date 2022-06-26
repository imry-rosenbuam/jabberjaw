import numpy as np
import pandas as pd
from jabberjaw.utils.calendars import HolidayCalenadr
from jabberjaw.utils.instrument import Instrument, instrument
from dataclasses import dataclass
from jabberjaw.utils.mkt_classes import MktCoord
from jabberjaw.utils.mkt import Mkt
from datetime import date

@dataclass
class IRIndex(Instrument):
    symbol: str = None
    lag: int = 2
    
    def __post_init__(self):
        super().__post_init__("ir_index")
        self._mkt_coord = MktCoord("IR",self.ccy,self.symbol)
        self._settlement_date = HolidayCalenadr.settle_date(self.calendar_conventions, self.mkt.ref_date,1)

    def price(self) -> float:
        return self.mkt.get_mkt_data(self._mkt_coord)

    def ir_yield(self) -> float:
        return self.price()
        
if __name__ == "__main__":
    dt = date(year=2022, month=1, day=3)
    mkt = Mkt(ref_date=dt)
    idx = IRIndex(mkt, ccy="USD",symbol= "PRIME-LOAN-RATE")
    print(idx.price())
    print("Le Fin")

