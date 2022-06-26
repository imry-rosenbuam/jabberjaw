from pandas import DataFrame
from jabberjaw.data_manager.data_reader import *


# These classes are in charge of extracting
class DataExtractorError(Exception):
    """raises a DataSource related exception"""


class DataExtractor(ABC):
    """ This is the template for the extractors.
    source: which determines what is the source we are trying to download from
     data_reader: the data reader that we use in order to download the data"""

    def __init__(self):
        self._source = None
        self._data_reader = DataReader()

    @property
    def source(self) -> str:
        return self._source

    @property
    def data_reader(self):
        return self._data_reader

    @abstractmethod
    def load_data(self, ticker) -> DataFrame:
        raise DataExtractorError("load data not implemented")

    @abstractmethod
    def load_eod_data(self, ticker, start: datetime.datetime = datetime.datetime.today(),
                      end: datetime.datetime = datetime.datetime.today(), ) -> DataFrame:
        raise DataExtractorError("load data not implemented")

    @abstractmethod
    def load_tick_data(self, ticker) -> DataFrame:
        raise DataExtractorError("load data not implemented")


class DataExtractorYahoo(DataExtractor):
    """Yahoo Data Extracotr"""
    def __init__(self):
        self._source = "yahoo"
        self._data_reader = DataReaderPD

    def load_eod_data(self, ticker, start: datetime.datetime = datetime.datetime.today(),
                      end: datetime.datetime = datetime.datetime.today()) -> DataFrame:
        return self.data_reader.download_data_eod(ticker, self._source, start, end)

    def load_data(self, ticker) -> DataFrame:
        pass

    def load_tick_data(self, ticker) -> DataFrame:
        pass


class DataExtractorMorningStar(DataExtractor):
    """morningstar Data Extractor"""
    def __init__(self):
        self._source = "morningstar"
        self._data_reader = DataReaderPD

    def load_eod_data(self, ticker, start: datetime.datetime = datetime.datetime.today(),
                      end: datetime.datetime = datetime.datetime.today()) -> DataFrame:
        return self.data_reader.download_data_eod(ticker, self._source, start, end)

    def load_data(self, ticker) -> DataFrame:
        pass

    def load_tick_data(self, ticker) -> DataFrame:
        pass
    
class DataExtractorFred(DataExtractor):
    """morningstar Data Extractor"""
    def __init__(self):
        self._source = "fred"
        self._data_reader = DataReaderPD

    def load_eod_data(self, ticker, start: datetime.datetime = datetime.datetime.today(),
                      end: datetime.datetime = datetime.datetime.today()) -> DataFrame:
        return self.data_reader.download_data_eod(ticker, self._source, start, end)

    def load_data(self, ticker) -> DataFrame:
        pass

    def load_tick_data(self, ticker) -> DataFrame:
        pass
