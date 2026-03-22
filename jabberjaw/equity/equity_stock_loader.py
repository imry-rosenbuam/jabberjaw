from jabberjaw.data_manager.data_loader import DataLoader
from jabberjaw.utils import mkt_classes as mkt_classes
import datetime
import polars as pl

sources = ["default", "morningstar"]

class EquityStockLoader(DataLoader):
    @classmethod
    def load_equity_market_data(cls, ticker: str, mkt_type: str, date: datetime.date) -> dict:
        mc = mkt_classes.parse_mkt_coord("equity_" + mkt_type + "_" + ticker)
        return cls.load_mkt_data(mc, date)

    @classmethod
    def load_equity_historical_market_data(cls, ticker: str, mkt_type: str) -> pl.DataFrame:
        mc = mkt_classes.parse_mkt_coord("equity_" + mkt_type + "_" + ticker)

        return cls.load_mkt_data_history(mc)

if __name__ == "__main__":
    dt = datetime.date(year=2020, month=11, day=17)
    print(EquityStockLoader.load_equity_market_data("pypl", "single stock", dt))
    print(EquityStockLoader.load_equity_historical_market_data("pypl", "single stock"))
