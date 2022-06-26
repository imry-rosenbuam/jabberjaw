import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from jabberjaw.utils.instrument import instrument,Instrument
from enum import Enum
from jabberjaw.utils.mkt import Mkt
from jabberjaw.utils.mkt_classes import MktCoord, tenor_parse
from jabberjaw.utils.calendars import DayCountConvention, HolidayCalenadr,  CalendarConventions
from datetime import date
from jabberjaw.ir.ir_curve import IRCurve
from dateutil import relativedelta

@instrument
class ZCBond(Instrument):
    calendar_conventions: CalendarConventions = None
    _par_value = 100
    _settlment_date: date = None
    yield_marked: bool = False
    curve_marked: bool = False
    curve: IRCurve = None
    
    def ir_yield(self) -> float:
        if self.yield_marked:
            data = self.mkt.get_mkt_data(self.mkt_coord)
            return data
        
        price = self.price()

        return (pow(self._par_value / price,-1 * HolidayCalenadr.daycount(self.calendar_conventions,self.mkt.ref_date, self._settlment_date)) - 1) * 100
    
    def price(self) -> float:
        if self.yield_marked:
            return 100 / np.exp(self.ir_yield() * self.daycount(self._settlment_date))
        
        if not self.curve_marked:
            return self.mkt.get_mkt_data(self.mkt_coord)
        
        return self.curve.discount_factor(self._settlment_date) * 100    
        
    def __post_init__(self, bond_type:str="standard",tenor:str = None, settlement_date=None):
        super().__post_init__("ZCBond")
        self.mkt_class = "IR"
        self.mkt_type = self.ccy
        self.mkt_asset = bond_type
        self.point = tenor if tenor else None

        self.calendar_conventions = CalendarConventions(dcc=DayCountConvention.ACT_360)
        self._settlement_date = self.mkt.ref_date + tenor_parse(tenor) if tenor else settlement_date
    
    @property
    def mkt_coord(self) -> MktCoord:
        if not isinstance(self._mkt_coord, MktCoord):
            self._mkt_coord = MktCoord(self.mkt_class, self.mkt_type, self.mkt_asset, self.point)
            xx = 1
        return self._mkt_coord
    

if __name__ == "__main__":
    dt = date(year=2020, month=11, day=16)
    mkt = Mkt(ref_date=dt)
    ZCBond(mkt,"USD")
    print("Le Fin")