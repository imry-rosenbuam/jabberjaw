from calendar import c
import numpy as np
import pandas as pd
import datetime
from dataclasses import dataclass
from jabberjaw.instruments.ir.zcbond import ZCBond
from datetime import date
from jabberjaw.utils.mkt import Mkt
tenors = [   "1M"
            ,"3M"
            ,"6M"
            ,"1Y" # to here is t-bill
            ,"2Y"
            ,"3Y"
            ,"5Y"
            ,"7Y"
            ,"10Y" # to here is t-notes
            ,"20Y"
            ,"30Y"]

@dataclass
class TreasuryCM(ZCBond):
    tenor : str = None
    
    def __post_init__(self,bond_type="TREASURY-CM"):
        super().__post_init__(bond_type=bond_type,tenor=self.tenor)
        if self.tenor not in tenors:
            raise "tenor is not recognised"
        self.yield_marked = True
        self._instrument_type = "BOND_TSY"


if __name__ == "__main__":
    dt = date(year=2022, month=1, day=3)
    mkt = Mkt(ref_date=dt)
    paper = TreasuryCM(mkt,"USD",tenor="3M")
    print(paper.bond_yield())
    print(paper.price())
    print("Le Fin")