import numpy as np
import polars as pl
from datetime import datetime as dt, timedelta, date, time
import datetime
from jabberjaw.utils.mkt_classes import MktCoord
from jabberjaw.utils.portfolio import Portfolio
from jabberjaw.utils.mkt import Mkt, Mkt_Factory
from dateutil.relativedelta import relativedelta


def optimal_future_hedge(time: date, horizon: relativedelta, future: MktCoord, spot: MktCoord, h=None) -> float:
    q_a = 1  # quantity of the spot to be hedged
    q_f = 1  # quantity of one contract future
    hr = h if h else optimal_future_hedge(time, horizon, future, spot)  # optimal hedge ratio calculated over the provided horizon

    return q_a * hr / q_f


#TODO: the spot should be changed to a portfolio
# but that will require updating the portfolio setup to also load the historical values
def optimal_hedege_ratio(end_date: date, horizon: relativedelta, future: MktCoord, spot: MktCoord) -> float:
    mkt: Mkt = Mkt_Factory.get_MKT()
    mkt.ref_date = end_date

    backdate = (dt.combine(end_date, time.min) - horizon).date()

    future_hist: pl.DataFrame = mkt.get_mkt_history(future, backdate).with_columns(
        pl.all().pct_change()
    ).slice(1)
    spot_hist: pl.DataFrame = mkt.get_mkt_history(spot, backdate).with_columns(
        pl.all().pct_change()
    ).slice(1)

    fut_series = future_hist["ADJ CLOSE"]
    pos_series = spot_hist["ADJ CLOSE"]

    fut_var = fut_series.std()
    pos_var = pos_series.std()

    cor = pl.DataFrame({"a": fut_series, "b": pos_series}).select(
        pl.corr("a", "b")
    ).item()

    h = cor * pos_var / fut_var

    return h


if __name__ == "__main__":
    cord_a = MktCoord('equity', 'single stock', 'amzn')
    cord_b = MktCoord("equity", "single stock", "amd")

    delta = relativedelta(years=5)
    end_date = date(year=2021, month=2, day=1)

    h = optimal_hedege_ratio(end_date, delta, cord_a, cord_b)
    print(h)
    print("Le Fin")
