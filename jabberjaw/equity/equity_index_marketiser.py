from jabberjaw.mkt_utils import data_manager as dm
from jabberjaw.mkt_utils import data_manager_parquet as dmp
from jabberjaw.mkt_utils import mkt_classes
import datetime

equity_tickers_to_marketsie = {
    "TESLA": ('TSLA', 'stock'),
    "SNP500": ('^GSPC', 'index')
}

source = "yahoo"


def marketise_equity_index_ticker(symbol: str,  ticker: str, category: str, start_date: datetime.date,
                                  end_date: datetime.date) -> None:
    df_new = dm.download_data_eod(ticker, source, datetime.datetime.fromordinal(start_date.toordinal()),
                                  datetime.datetime.fromordinal(end_date.toordinal()))
    mkt_str: str = "_".join(["equity", category, symbol, "spot"])
    mkt_coord: mkt_classes.MktCoord = mkt_classes.parse_mkt_coord(mkt_str)
    mkt_symbol: str = mkt_classes.mkt_symbol(mkt_coord)
    df = dmp.market_data_load(mkt_symbol)

    if not df.empty:
        df.update(df_new)
    else:
        df = df_new

    dmp.market_data_save(symbol, df)


def marketise_all_tickers(start_date: datetime, end_date: datetime.date) -> None:
    for k, v in equity_tickers_to_marketsie.items():
        marketise_equity_index_ticker(k, v[0], v[1], start_date, end_date)


if __name__ == '__main__':
    start = datetime.date(year=2016, month=1, day=1)
    end = datetime.date.today()
    marketise_all_tickers(start, end)
    x = 1
