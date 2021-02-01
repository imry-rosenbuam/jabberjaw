import jabberjaw.equity.equity_stock_extractor as ese
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
from typing import Union, Optional

ticker_list = ['XOM']


def complie_data(tckrs=None) -> Optional[pd.DataFrame]:

    tickers = tckrs.copy() if tckrs else ticker_list

    main_df: pd.DataFrame = pd.DataFrame()
    for ticker in tickers:
        df = ese.load_equity_cash_market_data(ticker)
        df.set_index('Date')
        df["bla"] = x
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)


def view_equity_cash_data(symbol: str) -> None:
    df = ese.load_equity_cash_market_data(symbol)

    style.use('ggplot')
    df.reset_index(inplace=True)
    df.set_index("Ref_Date", inplace=True)
    df['100 av'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()

    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()

    df_ohlc.reset_index(inplace=True)
    df_ohlc['ref_date'] = df_ohlc['ref_date'].map(lambda s: mdates.date2num(s.date()))

    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()

    candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='g')
    # ax2.fiill_between(df_volume.index.map(mdates.date2num), df_volume.values)
    plt.show()

    # ax1.plot(df.index, df['Adj Close'])
    # ax1.plot(df.index, df['100 av'])
    # ax2.bar(df.index, df['Volume'])


if __name__ == '__main__':
    ticker_ = "XOM"
    view_equity_cash_data(ticker_)

    x = 1
