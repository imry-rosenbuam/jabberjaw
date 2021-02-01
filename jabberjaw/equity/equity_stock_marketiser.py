from jabberjaw.mkt_utils import data_manager as dm
from jabberjaw.mkt_utils import data_manager_parquet as dmp
from jabberjaw.mkt_utils import mkt_classes
import datetime
import dpath.util as dpath
import jabberjaw.equity.equity_stock_extractor as equity_stock


def marketise_equity_index_ticker(ticker: str, source: str, start_date: datetime.date,
                                  end_date: datetime.date, overwrite: bool = False) -> None:

    mkt_c = mkt_classes.MktCoord('equity', 'stock', 'cash', (ticker,), source=source)

    mkt_symbol = mkt_c.mkt_symbol()

    df = dmp.market_data_load(mkt_symbol)

    if not df.empty and not overwrite:
        print(ticker + " already MARKETISED")
        return None

    print("TRYING to Marketise " + ticker)
    df_new = dm.download_data_eod(ticker, source, datetime.datetime.fromordinal(start_date.toordinal()),
                                  datetime.datetime.fromordinal(end_date.toordinal()))
    if df.empty:
        df = df_new
    else:
        df.update(df_new)
    dmp.market_data_save(mkt_symbol, df)


def marketise_all_tickers(start_date: datetime, end_date: datetime.date, overwrite: bool = False) -> None:
    mkt_cfg = mkt_classes.mkt_data_cfg()
    xpath = '{0}/{1}/{2}'.format("equity", "stock", "cash")
    equity_tickers_to_marketise = [i for i in dpath.search(mkt_cfg, xpath, yielded=True)].pop()[1]['points']
    source = [i for i in dpath.search(mkt_cfg, xpath, yielded=True)].pop()[1]['default_source']
    for k in equity_tickers_to_marketise:
        marketise_equity_index_ticker(k, source, start_date, end_date, overwrite=overwrite)


if __name__ == '__main__':
    start = datetime.date(year=2008, month=1, day=1)
    end = datetime.date.today()
    marketise_all_tickers(start, end)
    x = 1
