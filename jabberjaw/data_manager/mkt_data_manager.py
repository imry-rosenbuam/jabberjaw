from jabberjaw.data_manager.data_loader import DataLoader
from jabberjaw.equity import equity_stock_loader as equity_stock_loader
from jabberjaw.fx import fx_data_loader
from jabberjaw.mkt_utils.mkt_classes import MktCoord, get_mkt_types, get_mkt_assets, \
    get_points, get_mkt_class
from jabberjaw.data_manager.data_extractor import *

# data loaders for each of the asset classes and use-cases
data_loaders = {
    "none": DataLoader(),
    None: DataLoader(),
    "EQUITY": equity_stock_loader.EquityStockLoader(),
    "FX": fx_data_loader.FXDataLoader()
}

# a list of all possible extractors for the different sources
sources = {
    "yahoo": DataExtractorYahoo,
    "morningstar": DataExtractorMorningStar
}


class DataExtractorFactory:
    """ extractors factory class"""
    @classmethod
    def get_data_extractor(cls, source: str, usecase: str = None, **kwargs) -> DataExtractor:
        """ extractor factory method"""
        if source.lower() in sources:
            extractor = sources[source.lower()]
            if issubclass(extractor, DataExtractor):
                return extractor(**kwargs)
            else:
                if usecase and usecase in extractor.keys():
                    return extractor[usecase](**kwargs)
                else:
                    raise DataExtractorError("Non existent use-case provided to DataExtractor factory")

        else:
            raise DataExtractorError("Failed to find source in registered list")


class DataLoaderFactory:
    """ a factory for retrieving DataLoaders"""
    @classmethod
    def get_loader(cls, mkt_coord: MktCoord) -> DataLoader:
        """ the factory method for DataLoaders"""
        return data_loaders.get(mkt_coord.mkt_class)


def get_data_loader(mkt_coord: MktCoord):
    """ returns the data loader for MktCoord"""

    if mkt_coord.mkt_class not in get_mkt_class():
        raise Exception("failed to have a asset_class to load")

    if mkt_coord.mkt_type not in get_mkt_types(mkt_coord):
        raise Exception("failed to find asset in known list")

    if mkt_coord.mkt_asset not in get_mkt_assets(mkt_coord):
        raise Exception("failed to find category in known list")

    if not set(mkt_coord.points).issubset(get_points(mkt_coord)):
        raise Exception("Points provided are not recognized")

    data_loader: DataLoader = DataLoaderFactory.get_loader(mkt_coord)

    if not isinstance(data_loader, DataLoader):
        raise Exception("Returned DataLoader is not of type DataLoader")

    return data_loader


def get_mkt_data(mkt_coord: MktCoord, ref_date: datetime.date, obs_time: datetime.datetime = None) -> dict:
    """
    returns the mkt data for a refdate

    :param mkt_coord: mkt coordinate for which we return the data
    :param ref_date: date for which we return the date
    :param obs_time: latest acceptable observation time
    :return: a dict containing the market data
    """

    data_loader = get_data_loader(mkt_coord)
    return data_loader.load_mkt_data(mkt_coord, ref_date, obs_time)


def get_history_mkt_data(mkt_coord: MktCoord) -> pd.DataFrame:
    """ gets the complete time series for a MktCoord"""
    data_loader = get_data_loader(mkt_coord)
    return data_loader.load_mkt_data_history(mkt_coord)


def save_mkt_data(mkt_coord: MktCoord, df: pd.DataFrame):
    """ saves the market data given a MktCoord"""
    DataLoader.save_data(mkt_coord, df)


def extract_data(ticker: str, source: str, start: datetime.datetime, end: datetime.datetime):
    """extract the data from external source"""
    extractor = DataExtractorFactory.get_data_extractor(source)
    return extractor.load_eod_data(ticker, start, end)


if __name__ == '__main__':
    print("Le Fin")
