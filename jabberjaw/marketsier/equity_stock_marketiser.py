import datetime
import dpath.util as dpath
from jabberjaw.mkt_utils import mkt_classes
from jabberjaw.data_manager.marketiser import Marketiser


class EquityStockMarketiser(Marketiser):

    @classmethod
    def marketise_equity_stock_ticker(cls, ticker: str, source: str, start_date: datetime.date,
                                      end_date: datetime.date, overwrite: bool = False) -> None:
        mkt_c = mkt_classes.MktCoord('equity', 'single stock', ticker, source=source)

        cls.marketise_mkt_point(mkt_c, start_date, end_date,overwrite=overwrite)

    @classmethod
    def marketise_all_tickers_for_stock_cash(cls, start_date: datetime, end_date: datetime.date, overwrite: bool = False) -> None:
        """
        This function marketise all tickers for cash stocks
        :parm start_date: the date from which we marketise
        :parm end_date: the date will which we marketise (inclusive)
        :parm overwrite: a flag that determines if we overwrite existing data or not
        """
        mkt_cfg = mkt_classes.mkt_data_cfg()
        xpath = '{0}/{1}'.format("equity", "single stock").upper()
        search = dpath.search(mkt_cfg, xpath, yielded=True)
        equity_tickers_to_marketise = [i for i in search].pop()[1] # let us dump all the tickers and their metadata

        for ticker, metadata in equity_tickers_to_marketise.items():
            cls.marketise_equity_stock_ticker(ticker, metadata['default_source'], start_date, end_date, overwrite=overwrite)

        print('finished the marketisiation process for {}'.format(xpath))


if __name__ == '__main__':
    start = datetime.date(year=2000, month=1, day=1)
    end = datetime.date.today()
    EquityStockMarketiser.marketise_all_tickers_for_stock_cash(start, end)
    print('Le Fin')

