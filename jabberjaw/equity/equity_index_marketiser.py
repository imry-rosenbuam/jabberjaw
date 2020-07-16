import mkt_utils.yahoo_data_manager as ydm
import mkt_utils.data_manager_parquet as dmp
import datetime

equity_tickers_to_marketsie = {
    "TESLA": 'TSLA',
    "SNP500": '^GSPC'
}


def marketise_equity_index_ticker(symbol: str, ticker: str, start_date: datetime.date, end_date: datetime.date) -> None:
    df_new = ydm.download_data(ticker, datetime.datetime.fromordinal(start_date.toordinal()),
                               datetime.datetime.fromordinal(end_date.toordinal()))
    df = dmp.market_data_load(symbol)

    if not df.empty:
        df.update(df_new)
    else:
        df = df_new

    dmp.market_data_save(symbol, df)


def marketise_all_tickers(start_date: datetime, end_date: datetime.date) -> None:
    for k, v in equity_tickers_to_marketsie.items():
        marketise_equity_index_ticker(k, v, start_date, end_date)


