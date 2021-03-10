import datetime
import dpath.util as dpath
from jabberjaw.data_manager import mkt_data_manager as dm
from jabberjaw.mkt_utils import mkt_classes


def marketise_equity_index_ticker(ticker: str, source: str, start_date: datetime.date,
                                  end_date: datetime.date, overwrite: bool = False) -> None:
    mkt_c = mkt_classes.MktCoord('equity', 'stock', 'cash', (ticker,), source=source)
    df = dm.get_history_mkt_data(mkt_c)

    if not df.empty and not overwrite:
        print(ticker + " already MARKETISED")
        return None

    print("TRYING to Marketise " + ticker)
    df_new = dm.extract_data(ticker, source, datetime.datetime.fromordinal(start_date.toordinal()),
                             datetime.datetime.fromordinal(end_date.toordinal()))
    if df.empty:
        df = df_new
    else:
        df.update(df_new)

    dm.save_mkt_data(mkt_c, df)


def marketise_all_tickers(start_date: datetime, end_date: datetime.date, overwrite: bool = False) -> None:
    mkt_cfg = mkt_classes.mkt_data_cfg()
    xpath = '{0}/{1}/{2}'.format("equity", "stock", "cash").upper()
    search = dpath.search(mkt_cfg, xpath, yielded=True)
    equity_tickers_to_marketise = [i for i in search].pop()[1]['points']
    source = [i for i in dpath.search(mkt_cfg, xpath, yielded=True)].pop()[1]['default_source']
    for k in equity_tickers_to_marketise:
        marketise_equity_index_ticker(k, source, start_date, end_date, overwrite=overwrite)


if __name__ == '__main__':
    start = datetime.date(year=2000, month=1, day=1)
    end = datetime.date.today()
    marketise_all_tickers(start, end)
    print('Le Fin')
