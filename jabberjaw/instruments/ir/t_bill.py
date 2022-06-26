from calendar import c
import numpy as np
import pandas as pd
import datetime
from dataclasses import dataclass
from jabberjaw.instruments.ir.zcbond import ZCBond
from datetime import date
from jabberjaw.utils.mkt import Mkt
tenors = [ "4WK","3M","6M","1Y"]

@dataclass
class TBill(ZCBond):
    tenor : str = None
    
    def __post_init__(self,bond_type="T-BILL"):
        super().__post_init__(bond_type=bond_type,tenor=self.tenor)
        if self.tenor not in tenors:
            raise "tenor is not recognised"
        self.yield_marked = True
        self._instrument_type = "T-BILL"


if __name__ == "__main__":
    dt = date(year=2022, month=1, day=3)
    mkt = Mkt(ref_date=dt)
    paper = TBill(mkt,"USD",tenor="3M")
    print(paper.bond_yield())
    print(paper.price())
    print("Le Fin")