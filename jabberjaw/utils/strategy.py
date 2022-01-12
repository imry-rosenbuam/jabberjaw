from types import FunctionType
import numpy as np
import pandas as pd
from dataclasses import dataclass,field
from jabberjaw.utils.portfolio import Portfolio
from types import FunctionType
from jabberjaw.utils.instrument import Instrument
from typing import Optional,Dict
from jabberjaw.utils.mkt import Mkt
from jabberjaw.utils.instrument import DummyInstrument,DummyPricer
import datetime

@dataclass
class Strategy():
    portfolio:Portfolio
    x: FunctionType
    
    def __post_init__(self):
        pass


if __name__ == "__main__":
    xxx = Portfolio("imry is cool")
    pricer = DummyPricer()
    inst = DummyInstrument("EUR",pricer=pricer)
    #we need to make instrument into a hashable Function
    #let us explore the hashing function such that it will be scaleable
    pos = {inst:1}
    xxx.update_positions(pos)
    xx = Strategy(xxx, lambda s:1)
    
    print("Le   Fin")