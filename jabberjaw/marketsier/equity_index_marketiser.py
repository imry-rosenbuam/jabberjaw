import datetime
from jabberjaw.utils import mkt_classes
from jabberjaw.data_manager.marketiser import Marketiser


class EquityIndexMarketiser(Marketiser):
    @classmethod
    def mkt_class(cls) -> str:
        return "equity".upper()

    @classmethod
    def mkt_type(cls) -> str:
        return "index".upper()
    
if __name__ == "__main__":
    start = datetime.date(year=2000, month=1, day=1)
    end = datetime.date.today()
    EquityIndexMarketiser.marketise_all_mkt_type_tickers(start, end,overwrite=True)
    print('Le Fin')