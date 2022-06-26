from dataclasses import dataclass, field
from re import template
import pandas as pd
import numpy as np
from jabberjaw.utils.calendars import CalendarConventions, HolidayCalenadr
from jabberjaw.utils.mkt import Mkt
from typing import Optional
from jabberjaw.utils.mkt_classes import MktCoord
import datetime
from datetime import date
from abc import ABC, abstractclassmethod, abstractmethod
from jabberjaw.utils.helper_classes import Serializable
from jabberjaw.utils.calendars import CalendarConventions

def instrument(func):
    return dataclass(func)


@dataclass
class Instrument(Serializable,ABC):
    """base implementation of an instrument classs

    Raises:
        Exception: pricing  without a market
        Exception: pricing without a pricer setup

    Returns:
        price:  reutrn the price of the insturment

    """

    mkt: Mkt = None
    ccy: str = None
    _ccy: str = field(default="", init=False, repr=False)
    _mkt: Mkt = field(default=None, init=False, repr=False)
    _calendar_conventions: CalendarConventions = None  
    _mkt_coord: MktCoord = field(default=None, init=False, repr=False)
    _settlement_date: date = field(default=None, init = False)
    
    def __post_init__(self, inst_type: str):
        if self.ccy == "" or inst_type is None:
            raise "User failed to give ccy or instrument type to instrument instance"
        self._instrument_type = inst_type
        self._calendar_conventions = CalendarConventions()
    
    @property
    def calendar_conventions(self) -> CalendarConventions:
        return self._calendar_conventions
    
    @property
    def instrument_type(self) -> str:
        return self._instrument_type

    @property
    def ccy(self) -> str:
        return self._ccy

    @ccy.setter
    def ccy(self, ccy: str):
        if isinstance(ccy, str):
            self._ccy = ccy.upper()
        else:
            self._ccy = ""

    @abstractmethod
    def price(self) -> float:
        pass

    def dp(self) -> float:

        if self.mkt == None:
            raise Exception("Trying to price without a mkt")

        fx_pair = MktCoord("FX", "CURRENCY PAIR", self.ccy.upper()+"USD")
        fx_rate = 1 if self.ccy.upper() == "USD" else self.mkt.get_mkt_data(fx_pair)

        return self.price() * fx_rate

    def daycount(self, dt: datetime.date) -> float:
        return HolidayCalenadr.daycount(self.calendar_conventions, self.mkt.ref_date, dt)
        
    def __hash__(self) -> int:
        s = sum([hash(x) for x in self.__dict__.values()])
        return s
    
    @property
    def settlement_date(self) -> date:
        if not self._settlement_date:
            raise "Set Date has not been impolemented"
        return self._settlement_date
    @property
    def mkt_coord(self) -> MktCoord:
        return self._mkt_coord
    
@instrument
class DummyInstrument(Instrument):
        
    def __post_init__(self):
        super().__post_init__("DummyInst")
        print("Set up the dummy instrument")

    def price(self):
        return 1


if __name__ == "__main__":
    dt = datetime.date(year=2020, month=11, day=16)
    mkt = Mkt(ref_date=dt)
    instr = DummyInstrument(mkt=mkt, ccy="EUR")
    dp = instr.dp()
    print(f"dollar price is {dp}")
    print("Le Fin")
