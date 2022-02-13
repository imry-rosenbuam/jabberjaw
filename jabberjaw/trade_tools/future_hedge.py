import numpy as np
import pandas as pd
import scipy as sp
from datetime import datetime, timedelta, date
from jabberjaw.utils.mkt_classes import MktCoord
from jabberjaw.utils.portfolio import Portfolio
from jabberjaw.utils.mkt import Mkt, Mkt_Factory
from dateutil import relativedelta

def optimal_future_hedge(time: date,horizon: relativedelta, future: MktCoord, position:Portfolio,  h  = None) -> float:
    q_a = 1 # quantity of the position to be hedeged
    q_f = 1 # quantity of one contract future
    hr = h if h else optimal_future_hedge(time, horizon, future, position)  # optimal hedge ratio calculated over the provided horizon
    
    return q_a * hr / q_f


def optimal_hedege_ratio(end_date: date, horizon: relativedelta, future: MktCoord, position: Portfolio) -> float:
    mkt:Mkt = Mkt_Factory.get_MKT()
    mkt.ref_date = end_date
    backdate = (datetime.combine(end_date, datetime.min()) - horizon).date
    
    future_hist = mkt.get_mkt_history(future, backdate)
    
    
    return 1


if __name__ == "__main__":
    
    print("Le Fin")