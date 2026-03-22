from jabberjaw.equity.equity_stock_loader import EquityStockLoader
import matplotlib.pyplot as plt
from matplotlib import style
import polars as pl
from typing import Union, Optional

ticker_list = ['XOM']


def complie_data(tckrs=None) -> Optional[pl.DataFrame]:
    tickers = tckrs.copy() if tckrs else ticker_list

    main_df: pl.DataFrame = pl.DataFrame()
    for ticker in tickers:
        df = EquityStockLoader.load_equity_historical_market_data(ticker, "single stock")
        df = df.with_columns([
            ((pl.col('High') - pl.col('Low')) / pl.col('Low')).alias(f'{ticker}_HL_pct_change'),
            ((pl.col('Close') - pl.col('Open')) / pl.col('Open')).alias(f'{ticker}_daily_change'),
        ])
        df = df.rename({'Adj Close': ticker})
        df = df.drop(['High', 'Open', 'Close', 'Low', 'Volume'])
        if main_df.is_empty():
            main_df = df
        else:
            main_df = main_df.join(df, on='Ref_Date', how='left')

    return main_df


def view_data_frame(df_in: pl.DataFrame, index: str, column: str,
                    label: str = 'About as simple as it gets, folks') -> None:
    df = df_in.clone()
    style.use('ggplot')

    ax: plt.subplot = plt.subplot()
    ax.plot(df[index], df[column])

    ax.set(xlabel=index, ylabel=column, title=label)
    plt.show()


def view_data_frame_multi(df_in: pl.DataFrame, index: str, columns: list,
                          label: str = 'About as simple as it gets, folks', ylabel: str = "Thats it") -> None:
    df = df_in.clone()
    style.use('ggplot')

    ax: plt.subplot = plt.subplot()
    for column in columns:
        ax.plot(df[index], df[column], label=column)

    ax.legend(loc='upper left', shadow=True, fontsize='medium')
    ax.set(xlabel=index, ylabel=ylabel, title=label)
    plt.show()


def view_equity_cash_data(symbol: str) -> None:
    df = EquityStockLoader.load_equity_historical_market_data(symbol, "single stock")
    view_data_frame_multi(df, 'Ref_Date', ['Adj Close', 'Open'])


def view_equity_compiled_data(symbols: list = None) -> None:
    if symbols is None:
        symbols = ticker_list

    columns = [f'{ticker}_daily_change' for ticker in symbols]
    df = complie_data(symbols)
    view_data_frame_multi(df, 'Ref_Date', [columns])


if __name__ == '__main__':
    view_equity_compiled_data()
