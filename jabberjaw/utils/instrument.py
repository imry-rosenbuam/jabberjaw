from dataclasses import dataclass, field
from re import template
import pandas as pd
import numpy as np
from jabberjaw.utils.mkt import Mkt
from typing import Optional
from mkt_classes import MktCoord
import datetime

class Pricer:
    """
        base implementation of the pricer class
    """
    @classmethod
    def price(mkt: Mkt) -> float:
        raise Exception("Pricer price has not been implemented yet")


@dataclass
class Instrument:
    """base implementation of an instrument class

    Raises:
        Exception: pricing  without a market
        Exception: pricing without a pricer setup

    Returns:
        price:  reutrn the price of the insturment

    """
    ccy: str
    _ccy: str = field( init=False, repr=False)
    mkt: Mkt = None
    _mkt: Mkt = field(default=None, init=False, repr=False)
    pricer: Pricer = None
    _pricer: Pricer = field(default=None, init=False, repr=False)

    @property
    def ccy(self) -> str:
        return self._ccy
    
    @ccy.setter
    def ccy(self, ccy:str):
        self._ccy = ccy.upper()
    
    @property
    def pricer(self) -> Pricer:
        return self._pricer
    
    @pricer.setter
    def pricer(self, pricer:Pricer):
        self._pricer = pricer
    
    def price(self, mkt_input: Mkt = None) -> float:
        pricing_mkt = self.mkt if mkt_input == None else mkt_input

        if pricing_mkt == None:
            raise Exception("Trying to price without a mkt")
        elif self.pricer == None:
            raise Exception("Trying to price without a pricer")

        return self.pricer.price(pricing_mkt)

    def dp(self, mkt_input: Mkt = None) -> float:
        pricing_mkt = self.mkt if mkt_input == None else mkt_input

        if pricing_mkt == None:
            raise Exception("Trying to price without a mkt")
        
        fx_pair = MktCoord("FX", "CURRENCY PAIR", self.ccy.upper()+"USD")
        fx_rate = 1 if self.ccy.upper() == "USD" else pricing_mkt.get_mkt_data(fx_pair)

        return self.price(pricing_mkt) * fx_rate


class DummyPricer(Pricer):
    @classmethod
    def price(cls,mkt: Mkt) -> float:
        return 1

@dataclass
class DummyInstrument(Instrument):
    
    def __post_init__(self):
        print("Set up the dummy instrument")



if __name__ == "__main__":
    dt = datetime.date(year=2020, month=11, day=16)
    mkt = Mkt(_ref_date=dt)
    instr = DummyInstrument("EUR",mkt=mkt,pricer=DummyPricer())
    dp = instr.dp()
    print(f"dollar price is {dp}")
    print("Le Fin")
