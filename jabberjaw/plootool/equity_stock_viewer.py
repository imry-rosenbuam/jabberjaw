import jabberjaw.equity.equity_stock_loader as ese
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from typing import Union, Optional

ticker_list = ['XOM']


def complie_data(tckrs=None) -> Optional[pd.DataFrame]:
    tickers = tckrs.copy() if tckrs else ticker_list

    main_df: pd.DataFrame = pd.DataFrame()
    for ticker in tickers:
        df = ese.load_equity_cash_market_data(ticker)
        df.reset_index(inplace=True)
        df.set_index('Ref_Date', inplace=True)
        df['{}_HL_pct_change'.format(ticker)] = (df['High'] - df['Low']) / df['Low']
        df['{}_daily_change'.format(ticker)] = (df['Close'] - df['Open']) / df['Open']
        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['High', 'Open', 'Close', 'Low', 'Volume'], 1, inplace=True)
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    return main_df


def view_data_frame(df_in: pd.DataFrame, index: str, column: str,
                    label: str = 'About as simple as it gets, folks') -> None:
    df = df_in.copy(deep=True)
    style.use('ggplot')

    df.reset_index(inplace=True)
    df.set_index(index, inplace=True)

    ax: plt.subplot = plt.subplot()
    ax.plot(df.index, df[column])

    ax.set(xlabel=index, ylabel=column,
           title=label)

    plt.show()


def view_data_frame_multi(df_in: pd.DataFrame, index: str, columns: list,
                          label: str = 'About as simple as it gets, folks', ylabel: str = "Thats it") -> None:
    df = df_in.copy(deep=True)
    style.use('ggplot')

    df.reset_index(inplace=True)
    df.set_index(index, inplace=True)

    ax: plt.subplot = plt.subplot()
    for column in columns:
        ax.plot(df.index, df[column], label=column)

    legend = ax.legend(loc='upper left', shadow=True, fontsize='medium')

    ax.set(xlabel=index, ylabel=ylabel,
           title=label)
    plt.show()


def view_equity_cash_data(symbol: str) -> None:
    df = ese.load_equity_cash_market_data(symbol)

    view_data_frame_multi(df, 'Ref_Date', ['Adj Close', 'Open'])


def view_equity_compiled_data(symbols: list = None) -> None:
    if symbols is None:
        symbols = ticker_list

    columns = list()
    for ticker in symbols:
        columns.append('{}_daily_change'.format(ticker))
    df = complie_data(symbols)

    view_data_frame_multi(df, 'Ref_Date', [columns])


if __name__ == '__main__':
    ticker_ = "XOM"
    view_equity_compiled_data()
    # view_equity_cash_data(ticker_)
