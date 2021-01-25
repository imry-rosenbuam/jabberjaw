import os
import yaml
import datetime
from .mkt_classes import MktCoord, DataExtractor, mkt_data_cfg, get_mkt_class,get_mkt_types,get_mkt_assets,get_points
from ..equity import equity_stock_extractor as equity_stock_extractor

extractors = {
    "none": DataExtractor(),
    None: DataExtractor(),
    "equity": equity_stock_extractor.EquityStockExtractor()
}


def get_extractor(mkt_coord: MktCoord) -> DataExtractor:
    return extractors.get(mkt_coord.mkt_class)


def get_mkt_data(mkt_coord: MktCoord, ref_date: datetime.date, obs_time: datetime.datetime = None) -> dict:
    """

    :param mkt_coord: mkt coordinate for which we return the data
    :param ref_date: date for which we return the date
    :param obs_time: latest acceptable observation time
    :return: a dict containing the market data
    """
    if mkt_coord.mkt_class not in get_mkt_assets():
        raise Exception("failed to have a asset_class to load")

    if mkt_coord.mkt_type not in get_mkt_types(mkt_coord):
        raise Exception("failed to find asset in known list")

    if mkt_coord.mkt_asset not in get_mkt_assets(mkt_coord):
        raise Exception("failed to find category in know list")

    if not set(mkt_coord.points).issubset(get_points(mkt_coord)) and mkt_coord.points is not None:
        raise Exception("Points provided are not recognized")

    extractor = get_extractor(mkt_coord)
    if not isinstance(extractor, DataExtractor):
        raise Exception("Returned extractor is not of type DataExtractor")

    return extractor.load_mkt_data(mkt_coord, ref_date, obs_time)
