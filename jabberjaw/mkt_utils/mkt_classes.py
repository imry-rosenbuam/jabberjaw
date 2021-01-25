from abc import ABC
from dataclasses import dataclass
import datetime
import os
from typing import Union
import copy
import yaml
import re

__path: str = os.environ['TSDB_DATA']

parser_regex = '^([A-Za-z0-9]*)(_[A-Za-z0-9]*)?(_[A-Za-z0-9]*)?(_\w*)?(\.[A-Za-z0-9]*)?(@[A-Za-z0-9]*)?'

if os.path.exists(__path  + 'market_coord_cfg.YAML'):
    with open(__path + 'market_coord_cfg.YAML', 'r+') as f:
        yml = yaml.load(f, Loader=yaml.FullLoader)
        if yml:
            __mkt_data_cfg = yml.get("market_coordinates", {})
            __mkt_defaults_cfg = yml.get("defaults", {})
        else:
            __mkt_data_cfg = {}
            __mkt_defaults_cfg = {}
else:
    __mkt_data_cfg = {}
    __mkt_defaults_cfg = {}


def mkt_data_cfg() -> dict:
    return __mkt_data_cfg


def mkt_defaults_cfg() -> dict:
    return __mkt_defaults_cfg


def tsdb_path() -> str:
    return __path


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
    mkt_class mkt_type  mkt_asset point(s) quote_style splitting char is _ and . for quote style and @ for source
    """
    mkt_class: str
    mkt_type: str
    mkt_asset: str
    points: tuple = None
    quote: str = None
    source: str = None

    def get_mkt_tuple(self) -> tuple:
        return self.mkt_class, self.mkt_type, self.mkt_asset, self.quote, self.source

    def copy(self):
        return copy.copy(self)

    def deepcopy(self):
        return copy.deepcopy(self)
    # def __copy__(self):
    #    return copy.copy(self)

    # def __deepcopy__(self, memodict={}):
    #    return copy.deepcopy(self)


def mkt_symbol(mkt_coord: MktCoord, source_override: str = None) -> str:
    if source_override:
        return "_".join(
            [mkt_coord.mkt_class, mkt_coord.mkt_type, mkt_coord.mkt_asset] + list(
                mkt_coord.points)) + "." + mkt_coord.quote + "@" + source_override
    elif mkt_coord.source.lower() != 'default':
        return "_".join(
            [mkt_coord.mkt_class, mkt_coord.mkt_type, mkt_coord.mkt_asset] + list(
                mkt_coord.points)) + "." + mkt_coord.quote + "@" + mkt_coord.source
    else:
        default_source = get_coord_default_source(mkt_coord)
        return "_".join([mkt_coord.mkt_class, mkt_coord.mkt_type, mkt_coord.mkt_asset] + list(
            mkt_coord.points)) + "." + mkt_coord.quote + "@" + default_source


def parse_mkt_coord(mkt_coord_str: str) -> MktCoord:
    """
     mkt_class asset mkt_type point(s) quote_style splitting char is _ and . for quote style and @ for a source

    :param mkt_coord_str: input string to be parsed according to the above rules
    :return:
    """
    match = re.match(parser_regex, mkt_coord_str).groups()

    source = "default" if not match[5] else match[5].replace('@', '').lower()
    quote_style = "default" if not match[4] else match[4].replace('.', '').lower()

    mkt_class = match[0].replace('_', '').lower()  # get type
    mkt_type = match[1].replace('_', '').lower() if match[1] else None  # get asset
    mkt_asset = match[2].replace('_', '').lower() if match[2] else None  # get class
    points = tuple(match[3][1:].lower().split('_')) if match[3] else None  # get point(s)

    return MktCoord(mkt_class, mkt_type, mkt_asset, points=points, quote=quote_style, source=source)


def get_coord_default_source(mkt_coord: MktCoord) -> Union[str, None]:
    if mkt_coord.mkt_asset.lower() in get_mkt_assets(mkt_coord):
        return mkt_data_cfg()[mkt_coord.mkt_class][mkt_coord.mkt_type][mkt_coord.mkt_asset]["default_source"]
    else:
        return None


class DataExtractor:

    @classmethod
    def load_mkt_data(cls, mkt_coord: MktCoord, ref_data: datetime.date, obs_time: datetime.datetime) -> dict:
        return dict()


def get_points(coord: MktCoord) -> list:
    if coord.mkt_type in get_mkt_assets(coord):
        return list(
            mkt_data_cfg()[coord.mkt_class][coord.mkt_type][coord.mkt_asset]["points"])
    else:
        return []


def get_mkt_assets(coord: MktCoord) -> list:
    if coord.mkt_type not in get_mkt_types(coord):
        return []
    else:
        return list(mkt_data_cfg()[coord.mkt_class][coord.mkt_type].keys())


def get_mkt_types(coord: MktCoord) -> list:
    if coord.mkt_class in get_mkt_class():
        return list(mkt_data_cfg()[coord.mkt_class].keys())
    else:
        return []


def get_mkt_class() -> list:
    """
    return a list of all mkt_classs
    """
    return list(mkt_data_cfg().keys())


if __name__ == "__main__":
    mkt_coord_str_1 = "equity_index_snp500_spot.bla@yahoo"
    match1 = re.match(parser_regex, mkt_coord_str_1).groups()
    mkt_c = parse_mkt_coord(mkt_coord_str_1)
    d = mkt_c.copy()
    x = 1
