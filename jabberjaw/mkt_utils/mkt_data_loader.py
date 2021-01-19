import os
import yaml
import datetime
from .mkt_classes import MktCoord, DataExtractor, mkt_data_cfg, get_archetypes, get_assets, get_categories, get_points
from ..equity import equity_index_extractor as equity_index_extractor

extractors = {
    "none": DataExtractor(),
    None: DataExtractor(),
    "equity": equity_index_extractor.EquityIndexExtractor()
}


def get_extractor(mkt_coord: MktCoord) -> DataExtractor:
    return extractors.get(mkt_coord.archetype)


def get_mkt_data(mkt_coord: MktCoord, ref_date: datetime.date, obs_time: datetime.datetime = None) -> dict:
    """

    :param mkt_coord: mkt coordinate for which we return the data
    :param ref_date: date for which we return the date
    :param obs_time: latest acceptable observation time
    :return: a dict containing the market data
    """
    if mkt_coord.archetype not in get_archetypes():
        raise Exception("failed to have a archetype to load")

    if mkt_coord.asset not in get_assets(mkt_coord):
        raise Exception("failed to find asset in known list")

    if mkt_coord.category not in get_categories(mkt_coord):
        raise Exception("failed to find category in know list")

    if not set(mkt_coord.points).issubset(get_points(mkt_coord)) and mkt_coord.points is not None:
        raise Exception("Points provided are not recognized")

    extractor = get_extractor(mkt_coord)
    if not isinstance(extractor, DataExtractor):
        raise Exception("Returned extractor is not of type DataExtractor")

    return extractor.load_mkt_data(mkt_coord, ref_date, obs_time)
