from abc import ABC
from dataclasses import dataclass
import datetime
import os
import yaml
import re

_path = os.environ['TSDB_DATA']

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
    asset: str
    category: str
    points: list = None
    quote: str = None
    source: str = None

    def get_mkt_tuple(self) -> tuple:
        return self.archetype, self.asset, self.category, self.quote, self.source


def parse_mkt_coord(mkt_coord_str: str) -> MktCoord:
    """
     archetype asset category point(s) quote_style splitting char is _ and . for quote style and @ for a source

    :param mkt_coord_str: input string to be parsed according to the above rules
    :return:
    """
    match = re.match(parser_regex, mkt_coord_str).groups()

    source = "default" if not match[5] else match[5].replace('@', '')
    quote_style = "default" if not match[4] else match[4].replace('@', '')

    archetype = match[0].replace('_', '')  # get type
    asset = match[1].replace('_', '') if match[1] else None  # get asset
    category = match[2].replace('_', '') if match[2] else None  # get class
    points = match[3][1:].split('_') if match[2] else None  # get point(s)

    return MktCoord(archetype, asset, category, points=points, quote=quote_style, source=source)


class DataExtractor:

    @classmethod
    def load_mkt_data(cls, mkt_coord: MktCoord, ref_data: datetime.date, obs_time: datetime.datetime) -> dict:
        return dict()


def get_points(coord: MktCoord):
    if coord.category in get_categories(coord):
        return list(
            mkt_data_cfg()[coord.archetype][coord.asset][coord.category]["points"])
    else:
        return []


def get_categories(coord: MktCoord):
    if coord.asset in get_assets(coord):
        dsf = 1
        return list(mkt_data_cfg()[coord.archetype][coord.asset].keys())
    else:
        return []


def get_assets(coord: MktCoord):
    if coord.archetype in get_archetypes():
        return list(mkt_data_cfg()[coord.archetype].keys())
    else:
        return []


def get_archetypes() -> list:
    """
    return a list of all archetypes
    """
    return list(mkt_data_cfg().keys())
