import yfinance as yf
import yahoofinancials
import pandas as pd
import datetime


# download from yahoo and convert it to the ref date and obs time schema
# in our case the schema is banal as we only have eod data
def download_data(ticker: str, start_date: datetime.datetime, end_date: datetime.datetime) -> pd.DataFrame:
    start = datetime.date.fromordinal(start_date.toordinal())
    end = datetime.date.fromordinal(end_date.toordinal())
    df = yf.download(ticker, start, end)

    timestamps = list(df.index)
    obs_times = list(map(lambda x: x + pd.Timedelta('1 days') + pd.Timedelta('-1 sec'),timestamps))
    index = pd.MultiIndex.from_arrays([timestamps, obs_times], names=["ref_date", "obs_time"])

    return pd.DataFrame(index=index, data=df.values, columns=df.columns)


