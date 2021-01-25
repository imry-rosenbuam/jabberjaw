import pandas_datareader as web
import pandas as pd
import datetime


# download from source and convert it to the ref date and obs time schema
# in our case the schema is banal as we only have eod data
def download_data_eod(ticker: str, source: str, start_date: datetime.datetime,
                      end_date: datetime.datetime) -> pd.DataFrame:
    df = web.DataReader(ticker, source, start_date, end_date)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)

    timestamps = list(df.index)
    obs_times = list(map(lambda x: x + pd.Timedelta('1 days') + pd.Timedelta('-1 sec'), timestamps))
    index = pd.MultiIndex.from_arrays([timestamps, obs_times], names=["ref_date", "obs_time"])

    return pd.DataFrame(index=index, data=df.values, columns=df.columns)


if __name__ == "__main__":
    tck = "WAB"
    strt = datetime.datetime(year=2010, month=1, day=1)
    end = datetime.datetime(year=2020, month=12, day=31)
    src = 'yahoo'
    d = download_data_eod(tck, src, strt, end)

    x = 1
