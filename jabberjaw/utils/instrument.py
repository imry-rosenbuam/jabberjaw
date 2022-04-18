from dataclasses import dataclass, field
from re import template
import pandas as pd
import numpy as np
from jabberjaw.utils.mkt import Mkt
from typing import Optional
from jabberjaw.utils.mkt_classes import MktCoord
import datetime
from abc import ABC, abstractclassmethod, abstractmethod
from jabberjaw.utils.helper_classes import Serializable

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
    instrument_type: str = None
    _ccy: str = field(default="", init=False, repr=False)
    _instrument_type: str = field(default=None, init=False, repr=False)
    _mkt: Mkt = field(default=None, init=False, repr=False)

    def __post_init__(self, inst_type: str):
        if self.ccy == "" or inst_type is None:
            raise "User failed to give ccy or instrument type to instrument instance"
        self._instrument_type = inst_type
        
    @property
    def instrument_type(self) -> str:
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, inst: str):
        if isinstance(inst, str):
            raise "User should not set the instrument type outside of init"
            #self._instrument_type = inst
        else:
            self._instrument_type = None

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
    def price(self, mkt_input: Mkt = None) -> float:
        pass

    def dp(self) -> float:

        if self.mkt == None:
            raise Exception("Trying to price without a mkt")

        fx_pair = MktCoord("FX", "CURRENCY PAIR", self.ccy.upper()+"USD")
        fx_rate = 1 if self.ccy.upper() == "USD" else self.mkt.get_mkt_data(fx_pair)

        return self.price() * fx_rate

    def __hash__(self) -> int:
        s = sum([hash(x) for x in self.__dict__.values()])
        return s


@dataclass
class DummyInstrument(Instrument):

    def __post_init__(self):
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
