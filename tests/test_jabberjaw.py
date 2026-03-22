from jabberjaw import __version__
import polars as pl


def test_version():
    assert __version__ == '0.1.0'


if __name__ == "__main__":
    file_name = "hcpi_barnet.csv"
    path: str = "C:\\Users\\imryr\\imry_cpi.csv"
    full_path = path + file_name
    df = pl.read_csv(full_path)
    print(full_path)
    print(df.head())
