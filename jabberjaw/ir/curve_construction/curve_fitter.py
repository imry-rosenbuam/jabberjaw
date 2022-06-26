from tkinter import Y
import numpy as np
import pandas as pd
import yaml
import jabberjaw.utils.mkt_classes
from jabberjaw.utils.mkt import Mkt
import os
from jabberjaw.utils.instrument import Instrument
from jabberjaw.instruments.ir.commercial_paper import FinCommercialPaper, NonFinCommercialPaper
from jabberjaw.instruments.ir.irindex import IRIndex
from jabberjaw.instruments.ir.tsy_cm import TreasuryCM
from jabberjaw.instruments.ir.t_bill import TBill
from datetime import date
import matplotlib.pyplot as plt

file_path = "usd_curve_template.YAML"


class IRFactory():
    
    def __init__(self, mkt: Mkt):    
        self.mkt = mkt
    
    def create_ir_instrument(self, instrument: str, tenor:str = None, symbol:str = None, ccy ="USD") -> Instrument:
        inst = instrument.lower()
        sym = symbol.lower() if symbol else None
        mkt = self.mkt
        if inst == "ir_index":
            return IRIndex(mkt, symbol=symbol, ccy=ccy)
        elif inst == "commerical_paper":
            if sym == "financial":
                return FinCommercialPaper(mkt,tenor=tenor, ccy=ccy)
            else:
                return NonFinCommercialPaper(mkt, tenor=tenor, ccy=ccy)
        elif inst == "t_bill":
            return TBill(mkt, tenor=tenor, ccy=ccy)
        elif inst == "tsy_cm":
            return TreasuryCM(mkt, tenor=tenor, ccy=ccy)
        else:
            raise "Unkown Instrument specifications have been provided please review inputs"

if __name__ == "__main__":
    dt = date(year=2022, month=1, day=3)
    mkt = Mkt(ref_date=dt)
    
    with open(jabberjaw.utils.mkt_classes.tsdb_path() + file_path, 'r') as file:
        curve_template = yaml.safe_load(file)
    instruments = []
    fact = IRFactory(mkt)
    
    for name,inst in curve_template.get("USD",[]).items():
        pts = inst.get("points",[])
        symbol = inst.get("symbol",None)
        if len(pts):
            for pt in pts:
                instruments.append(fact.create_ir_instrument(inst["type"],pt,symbol))
        else:
            instruments.append(fact.create_ir_instrument(inst["type"],None,symbol))
    
    x_axis = []
    y_axis = []
    
    for i in instruments:
        print(f"{i.settlement_date}, {i.instrument_type}, {i.mkt_coord.mkt_symbol()}" )
        print(i.ir_yield())
        x_axis.append(i.settlement_date)
        y_axis.append(i.ir_yield())

    data = list(zip(x_axis,y_axis))
    data.sort(key=lambda x: x[0])
    xlabel, ylabel = zip(*data)
        
    #plt.plot(x = x_axis, y=y_axis)
    plt.plot(xlabel,ylabel)
    plt.xlabel('time')
    plt.ylabel("ir_yield")
    plt.title("usd yield curve")
    plt.show()
    xx = 155