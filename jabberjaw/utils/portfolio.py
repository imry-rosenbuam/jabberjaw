import pandas as pd
import numpy as np
from dataclasses import dataclass,field
from jabberjaw.utils.instrument import Instrument
from typing import Optional,Dict
from jabberjaw.utils.mkt import Mkt
from jabberjaw.utils.instrument import DummyInstrument,DummyPricer
import datetime

# let us define an alias for positions tracking
Position = Dict[Instrument,float]

@dataclass
class Portfolio:
    name: str
    _name: str = field(init=False, repr=False)
    positions: Position = None
    _positions: Position = field(default_factory=dict,init=False,repr=False)
    
    @property
    def positions(self):
        return self._positions
    
    @positions.setter
    def positions(self,positions:Position):
        if not isinstance(positions,property) and not positions is None:
            self._positions = positions
        else:
            self._positions = {}

    def update_positions(self, positions:Position):
        self.positions.update(positions)
    
    def value(self, mkt:Mkt) -> float:
        val = 0
        for instr, amount in self.positions.items():
            val += instr.price(mkt) * amount
        
if __name__ == "__main__":
    xxx = Portfolio("imry is cool")
    pricer = DummyPricer()
    inst = DummyInstrument("EUR",pricer=pricer)
    #we need to make instrument into a hashable Function
    #let us explore the hashing function such that it will be scaleable
    pos = {inst:1}
    xxx.update_positions(pos)
    dt = datetime.date(year=2020, month=11, day=16)
    mkt = Mkt(dt)
    print(xxx.value(mkt))
    print("Le Fin")
