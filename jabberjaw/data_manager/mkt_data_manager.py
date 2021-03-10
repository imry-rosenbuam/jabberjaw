from jabberjaw.data_manager.data_loader import DataLoader
from jabberjaw.equity import equity_stock_loader as equity_stock_loader
from jabberjaw.mkt_utils.mkt_classes import MktCoord, get_mkt_types, get_mkt_assets, \
    get_points, get_mkt_class
from jabberjaw.data_manager.data_extractor import *

data_loaders = {
    "none": DataLoader(),
    None: DataLoader(),
    "EQUITY": equity_stock_loader.EquityStockLoader()
}

sources = {
    "yahoo": DataExtractorYahoo,
    "morningstar": DataExtractorMorningStar
}


class DataExtractorFactory:
    @classmethod
    def get_data_extractor(cls, source: str, usecase: str = None, **kwargs) -> DataExtractor:
        if source in sources:
            extractor = sources[source]
            if issubclass(extractor, DataExtractor):
                return extractor(**kwargs)
            else:
                if usecase and usecase in extractor.keys():
                    return extractor[usecase](**kwargs)
                else:
                    raise DataExtractorError("Non existent usecase provided to DataExtractor factory")

        else:
            raise DataExtractorError("Failed to find source in registered list")


class DataLoaderFactory:
    @classmethod
    def get_loader(cls, mkt_coord: MktCoord) -> DataLoader:
        return data_loaders.get(mkt_coord.mkt_class)


def get_data_loader(mkt_coord: MktCoord):
    if mkt_coord.mkt_class not in get_mkt_class():
        raise Exception("failed to have a asset_class to load")

    if mkt_coord.mkt_type not in get_mkt_types(mkt_coord):
        raise Exception("failed to find asset in known list")

    if mkt_coord.mkt_asset not in get_mkt_assets(mkt_coord):
        raise Exception("failed to find category in know list")

    if not set(mkt_coord.points).issubset(get_points(mkt_coord)) and mkt_coord.points is not None:
        raise Exception("Points provided are not recognized")

    data_loader: DataLoader = DataLoaderFactory.get_loader(mkt_coord)

    if not isinstance(data_loader, DataLoader):
        raise Exception("Returned DataLoader is not of type DataLoader")

    return data_loader


def get_mkt_data(mkt_coord: MktCoord, ref_date: datetime.date, obs_time: datetime.datetime = None) -> dict:
    """

    :param mkt_coord: mkt coordinate for which we return the data
    :param ref_date: date for which we return the date
    :param obs_time: latest acceptable observation time
    :return: a dict containing the market data
    """

    data_loader = get_data_loader(mkt_coord)
    return data_loader.load_mkt_data(mkt_coord, ref_date, obs_time)


def get_history_mkt_data(mkt_coord: MktCoord) -> pd.DataFrame:
    data_loader = get_data_loader(mkt_coord)
    return data_loader.load_mkt_data_history(mkt_coord)


def save_mkt_data(mkt_coord: MktCoord, df: pd.DataFrame):
    DataLoader.save_data(mkt_coord, df)


def extract_data(ticker: str, source: str, start: datetime.datetime, end: datetime.datetime):
    extractor = DataExtractorFactory.get_data_extractor(source)
    return extractor.load_eod_data(ticker, start, end)


if __name__ == '__main__':
    print("Le Fin")
