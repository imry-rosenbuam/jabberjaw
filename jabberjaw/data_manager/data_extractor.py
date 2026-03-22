import datetime
import polars as pl
from abc import ABC, abstractmethod
from jabberjaw.data_manager.data_reader import DataReader, DataReaderYahoo, DataReaderFred


# These classes are in charge of extracting
class DataExtractorError(Exception):
    """raises a DataSource related exception"""


class DataExtractor(ABC):
    """ This is the template for the extractors.
    source: which determines what is the source we are trying to download from
     data_reader: the data reader that we use in order to download the data"""

    def __init__(self):
        self._source = None
        self._data_reader: DataReader = None

    @property
    def source(self) -> str:
        return self._source

    @property
    def data_reader(self):
        return self._data_reader

    @abstractmethod
    def load_data(self, ticker) -> pl.DataFrame:
        raise DataExtractorError("load data not implemented")

    @abstractmethod
    def load_eod_data(self, ticker, start: datetime.datetime = datetime.datetime.today(),
                      end: datetime.datetime = datetime.datetime.today()) -> pl.DataFrame:
        raise DataExtractorError("load data not implemented")

    @abstractmethod
    def load_tick_data(self, ticker) -> pl.DataFrame:
        raise DataExtractorError("load data not implemented")


class DataExtractorYahoo(DataExtractor):
    """Yahoo Finance Data Extractor"""
    def __init__(self):
        self._source = "yahoo"
        self._data_reader = DataReaderYahoo

    def load_eod_data(self, ticker, start: datetime.datetime = datetime.datetime.today(),
                      end: datetime.datetime = datetime.datetime.today()) -> pl.DataFrame:
        return self.data_reader.download_data_eod(ticker, start_date=start, end_date=end)

    def load_data(self, ticker) -> pl.DataFrame:
        pass

    def load_tick_data(self, ticker) -> pl.DataFrame:
        pass


class DataExtractorMorningStar(DataExtractor):
    """Morningstar Data Extractor (stub — source no longer supported)"""
    def __init__(self):
        self._source = "morningstar"
        self._data_reader = None

    def load_eod_data(self, ticker, start: datetime.datetime = datetime.datetime.today(),
                      end: datetime.datetime = datetime.datetime.today()) -> pl.DataFrame:
        raise DataExtractorError("Morningstar source is no longer supported")

    def load_data(self, ticker) -> pl.DataFrame:
        pass

    def load_tick_data(self, ticker) -> pl.DataFrame:
        pass


class DataExtractorFred(DataExtractor):
    """FRED Data Extractor"""
    def __init__(self):
        self._source = "fred"
        self._data_reader = DataReaderFred

    def load_eod_data(self, ticker, start: datetime.datetime = datetime.datetime.today(),
                      end: datetime.datetime = datetime.datetime.today()) -> pl.DataFrame:
        return self.data_reader.download_data_eod(ticker, start_date=start, end_date=end)

    def load_data(self, ticker) -> pl.DataFrame:
        pass

    def load_tick_data(self, ticker) -> pl.DataFrame:
        pass
