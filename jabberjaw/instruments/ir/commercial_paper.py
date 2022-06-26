from calendar import c
import numpy as np
import pandas as pd
import datetime
from dataclasses import dataclass
from jabberjaw.instruments.ir.zcbond import ZCBond
from datetime import date
from jabberjaw.utils.mkt import Mkt
tenors = ["1M", "2M", "3M"]

@dataclass
class CommericalPaper(ZCBond):
    tenor : str = None
    
    def __post_init__(self,bond_type="CommercialPaper", tenor=None):
        super().__post_init__(bond_type=bond_type,tenor=tenor)
        self.yield_marked = True
        
class FinCommercialPaper(CommericalPaper):
    tenor: str = None
    
    def __post_init__(self):
        super().__post_init__("COM-PAPER-F",self.tenor)
        if self.tenor not in tenors:
            raise "tenor is not recognised"
        self.yield_marked = True
        self._instrument_type = "COM-PAPER-F"
        
class NonFinCommercialPaper(CommericalPaper):
    tenor: str = None
    
    def __post_init__(self):
        super().__post_init__("COM-PAPER-NONF",self.tenor)
        if self.tenor not in tenors:
            raise "tenor is not recognised"
        self.yield_marked = True
        self._instrument_type = "COM-PAPER-NONF"

if __name__ == "__main__":
    dt = date(year=2022, month=1, day=3)
    mkt = Mkt(ref_date=dt)
    paper = FinCommercialPaper(mkt,"USD",tenor="1M")
    print(paper.bond_yield())
    print(paper.price())
    print("Le Fin")