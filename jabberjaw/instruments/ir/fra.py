import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from jabberjaw.utils.instrument import instrument,Instrument
from enum import Enum
from jabberjaw.utils.mkt import Mkt
from jabberjaw.utils.mkt_classes import MktCoord

def fra_direction(Enum):
    PAYER = object(),
    RECIEVER = object()

@instrument
class FRA(Instrument):
    notional: int = 1 
    rate_strike: float
    direction: fra_direction
    index = ""
    
    
    
    def __post_init__(self):
        self.index_mktc = MktCoord("IR","INDEX",self.index)  
        return super().__post_init__("FRA")

    def get_index_value(self) -> float:
        
        return self.mkt.get_mkt_data(self.index_mktc)
    
    def price(self, mkt_input: Mkt = None) -> float:
        direction = 1 if self.direction == fra_direction.PAYER else 0
        mkt = mkt_input if mkt_input else self.mkt
        
                    
        
if __name__ == "__init__":
    
    print("Le Fin")