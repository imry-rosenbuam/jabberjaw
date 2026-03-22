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
        raise NotImplementedError("FRA.price() is not yet implemented")

if __name__ == "__main__":
    
    print("Le Fin")