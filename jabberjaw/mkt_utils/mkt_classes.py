from abc import ABC
from dataclasses import dataclass
import datetime
import os
import yaml
import re

_path: str = os.environ['TSDB_DATA']

parser_regex = '^([A-Za-z0-9]*)(_[A-Za-z0-9]*)?(_[A-Za-z0-9]*)?(_\w*)?(\.[A-Za-z0-9]*)?(@[A-Za-z0-9]*)?'

with open(_path + 'market_coord_cfg.YAML') as f:
    _mkt_data_cfg = yaml.load(f, Loader=yaml.FullLoader).get("market_coordinates")


def mkt_data_cfg() -> dict:
    return _mkt_data_cfg


def tsdb_path() -> str:
    return _path


class Singleton(type, ABC):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            super()
        return cls._instances[cls]


class LocalSingleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


@dataclass
class MktCoord:
    """
    archetype asset category point(s) quote_style splitting char is _ and . for quote style and @ for source
    """
    archetype: str
    category: str
    asset: str
    points: list = None
    quote: str = None
    source: str = None

    def get_mkt_tuple(self) -> tuple:
        return self.archetype, self.category, self.asset, self.quote, self.source


def mkt_symbol(mkt_coord: MktCoord, source_override: str = None) -> str:
    if source_override:
        return "_".join([mkt_coord.archetype, mkt_coord.category, mkt_coord.asset, "."+mkt_coord.quote, "@"+source_override])
    elif mkt_coord.source.lower() != 'default':
        return "_".join([mkt_coord.archetype, mkt_coord.category, mkt_coord.asset, "."+mkt_coord.quote, "@"+mkt_coord.source])
    else:
        default_source = get_coord_default_source(mkt_coord)
        return "_".join([mkt_coord.archetype, mkt_coord.category, mkt_coord.asset, "."+mkt_coord.quote, "@"+default_source])


def parse_mkt_coord(mkt_coord_str: str) -> MktCoord:
    """
     archetype asset category point(s) quote_style splitting char is _ and . for quote style and @ for a source

    :param mkt_coord_str: input string to be parsed according to the above rules
    :return:
    """
    match = re.match(parser_regex, mkt_coord_str).groups()

    source = "default" if not match[5] else match[5].replace('@', '').lower()
    quote_style = "default" if not match[4] else match[4].replace('.', '').lower()

    archetype = match[0].replace('_', '').lower()  # get type
    category= match[1].replace('_', '').lower() if match[1] else None  # get asset
    asset = match[2].replace('_', '').lower() if match[2] else None  # get class
    points = match[3][1:].lower().split('_') if match[3] else None  # get point(s)

    return MktCoord(archetype, category, asset, points=points, quote=quote_style, source=source)


def get_coord_default_source(mkt_coord: MktCoord)->str:
    if mkt_coord.category.lower() in get_categories(mkt_coord):
        return mkt_data_cfg()[mkt_coord.archetype][mkt_coord.category][mkt_coord.asset]["default_source"]
    else:
        return None


class DataExtractor:

    @classmethod
    def load_mkt_data(cls, mkt_coord: MktCoord, ref_data: datetime.date, obs_time: datetime.datetime) -> dict:
        return dict()


def get_points(coord: MktCoord)->list:
    if coord.category in get_categories(coord):
        return list(
            mkt_data_cfg()[coord.archetype][coord.category][coord.asset]["points"])
    else:
        return []


def get_assets(coord: MktCoord)->list:
    if coord.category not in get_categories(coord):
        return []
    else:
        return list(mkt_data_cfg()[coord.archetype][coord.category].keys())


def get_categories(coord: MktCoord)->list:
    if coord.archetype in get_archetypes():
        return list(mkt_data_cfg()[coord.archetype].keys())
    else:
        return []


def get_archetypes() -> list:
    """
    return a list of all archetypes
    """
    return list(mkt_data_cfg().keys())

if __name__ =="__main__":
    mkt_coord_str = "equity_index_snp500_spot.bla@yahoo"
    match = re.match(parser_regex, mkt_coord_str).groups()
    x = 1