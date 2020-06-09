from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
import os
import yaml

_path = os.environ['TSDB_DATA']

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
    mkt_coord = mkt_coord_str.lower().split("@")
    source = "default" if len(mkt_coord) == 1 else mkt_coord.pop()
    mkt_coord = mkt_coord.pop()

    mkt_coord = mkt_coord.split(".")
    quote_style = "default" if len(mkt_coord) == 1 else mkt_coord.pop()
    mkt_coord = mkt_coord.pop().split("_")

    archetype = mkt_coord.pop(0)  # get type
    asset = mkt_coord.pop(0) if len(mkt_coord) else None  # get asset
    category = mkt_coord.pop(0) if len(mkt_coord) else None  # get class
    points = mkt_coord if len(mkt_coord) else None  # get point(s)

    return MktCoord(archetype, asset, category, points=points, quote=quote_style, source=source)


class DataExtractor:

    @classmethod
    def load_mkt_data(cls, mkt_coord: MktCoord, ref_data: datetime.date, obs_time: datetime.datetime) -> dict:
        return dict()


def get_points( coord: MktCoord):
    if coord.category in get_categories(coord):
        return list(
            mkt_data_cfg()[coord.archetype][coord.asset][coord.category]["points"])
    else:
        return []


def get_categories(coord: MktCoord):
    if coord.asset in get_assets(coord):
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