from abc import ABC
from dataclasses import dataclass, field
import datetime
import os
from typing import Union
import copy
import yaml
import re

__path: str = os.environ['TSDB_DATA']

parser_regex = '^([A-Za-z0-9\s]*)(_[A-Za-z0-9\s]*)?(_[A-Za-z0-9\s]*)?(_[\w\s]*)?(\.[A-Za-z0-9]*)?(@[A-Za-z0-9]*)?'

if os.path.exists(__path + 'market_coord_cfg.YAML'):
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
    """returns the config for mkt data coordinates"""
    return __mkt_data_cfg


def mkt_defaults_cfg() -> dict:
    """returns the config that defines defaults for the mkt coordinates"""
    return __mkt_defaults_cfg


def tsdb_path() -> str:
    """ returns the path to our data directory"""
    return __path


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@dataclass
class MktCoord:
    """
    mkt_class mkt_type  mkt_asset point(s) quote_style splitting char is _ and . for quote style and @ for source
    Note: this is a dataclass and as such does not have an __init__ method as it is generated at initialization
    """
    mkt_class: str
    _mkt_class: str = field(init=False, repr=False)
    mkt_type: str
    _mkt_type: str = field(init=False, repr=False)
    mkt_asset: str
    _mkt_asset: str = field(init=False, repr=False)
    points: tuple = tuple()
    _points: tuple = field(default=None, init=False, repr=False)
    quote: str = None
    _quote: str = field(default=None, init=False, repr=False)
    source: str = None
    _source: str = field(default=None, init=False, repr=False)

    def get_mkt_tuple(self) -> tuple:
        return self.mkt_class, self.mkt_type, self.mkt_asset, self.quote, self.source

    @property
    def mkt_class(self) -> str:
        return self._mkt_class

    @mkt_class.setter
    def mkt_class(self, mkt_class: str):
        self._mkt_class = mkt_class.upper()

    @property
    def mkt_type(self) -> str:
        return self._mkt_type

    @mkt_type.setter
    def mkt_type(self, mkt_type: str):
        self._mkt_type = mkt_type.upper()

    @property
    def mkt_asset(self) -> str:
        return self._mkt_asset

    @mkt_asset.setter
    def mkt_asset(self, mkt_asset: str):
        self._mkt_asset = mkt_asset.upper()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points: tuple):
        self._points = tuple([s.upper() for s in list(points)]) if (
            not isinstance(points, property)) and (points is not None) else tuple()

    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, source: str):
        self._source = str(source).upper() if not isinstance(
            source, property) else "default"

    @property
    def quote(self) -> str:
        return self._quote

    @quote.setter
    def quote(self, quote: str):
        self._quote = str(quote).upper() if not isinstance(
            quote, property) else None

    def copy(self):
        return copy.copy(self)

    def deepcopy(self):
        return copy.deepcopy(self)

    def mkt_symbol(self, source_override=None) -> str:
        """returns the mkt symbol for the MktCoord"""
        quote_string = '.' + \
            self.quote if not (
                self.quote == None or self.quote.lower() == "default") else ""
        source_string = "default" if not self.source else self.source.upper()
        if source_override:
            mkt_str = "_".join(
                [self.mkt_class, self.mkt_type, self.mkt_asset] + list(
                    self.points)) + quote_string + "@" + source_override
        elif source_string.upper() != 'default'.upper():
            mkt_str = "_".join(
                [self.mkt_class, self.mkt_type, self.mkt_asset] + list(
                    self.points)) + quote_string + "@" + source_string
        else:
            default_source = get_coord_default_source(self)
            mkt_str = "_".join([self.mkt_class, self.mkt_type, self.mkt_asset] + list(
                self.points)) + quote_string + "@" + default_source

        return mkt_str.upper()


def parse_mkt_coord(mkt_coord_str: str) -> MktCoord:
    """
     mkt_class mkt_type mkt_asset point(s) quote_style splitting char is _ and . for quote style and @ for a source

    :param mkt_coord_str: input string to be parsed according to the above rules
    :return:
    """
    match = re.match(parser_regex, mkt_coord_str.upper()).groups()

    source = "default".upper() if not match[5] else match[5].replace('@', '')
    quote_style = "default".upper(
    ) if not match[4] else match[4].replace('.', '')

    mkt_class = match[0].replace('_', '')  # get type
    mkt_type = match[1].replace('_', '') if match[1] else None  # get asset
    mkt_asset = match[2].replace('_', '') if match[2] else None  # get class
    points = tuple(match[3][1:].split(
        '_')) if match[3] else None  # get point(s)

    return MktCoord(mkt_class, mkt_type, mkt_asset, points=points, quote=quote_style, source=source)


def get_coord_default_source(mkt_coord: MktCoord) -> Union[str, None]:
    """returns the default source for a given MktCoord"""
    if mkt_coord.mkt_asset.upper() in [mkt_asset.upper() for mkt_asset in get_mkt_assets(mkt_coord)]:
        return mkt_data_cfg()[mkt_coord.mkt_class.upper()][mkt_coord.mkt_type.upper()][mkt_coord.mkt_asset.upper()][
            "default_source"].upper()
    else:
        return None


def get_ticker(coord: MktCoord) -> list:
    """return valid ticker for a MktCoord"""
    if coord.mkt_asset.upper() in [asset.upper() for asset in get_mkt_assets(coord)]:
        return mkt_data_cfg()[coord.mkt_class.upper()][coord.mkt_type.upper()][coord.mkt_asset.upper()].get("ticker", coord.mkt_asset.upper())


def get_points(coord: MktCoord) -> list:
    """ return the valid points for a MktCoord"""
    if coord.mkt_asset.upper() in [asset.upper() for asset in get_mkt_assets(coord)]:
        return list(
            mkt_data_cfg()[coord.mkt_class.upper()][coord.mkt_type.upper()][coord.mkt_asset.upper()]["points"])
    else:
        return []


def get_mkt_assets(coord: MktCoord) -> list:
    """ returns a list of valid mkt assets for a MktCoord"""
    if coord.mkt_type.upper() not in [mkt_type.upper() for mkt_type in get_mkt_types(coord)]:
        return []
    else:
        return list(mkt_data_cfg()[coord.mkt_class.upper()][coord.mkt_type.upper()].keys())


def get_mkt_types(coord: MktCoord) -> list:
    """ returns a lost of valid mkt-types for MktCoord"""
    if coord.mkt_class.upper() in [mkt_class.upper() for mkt_class in get_mkt_class()]:
        return list(mkt_data_cfg()[coord.mkt_class.upper()].keys())
    else:
        return []


def get_mkt_class() -> list:
    """
    return a list of all mkt_classs
    """
    return list(mkt_data_cfg().keys())


if __name__ == "__main__":
    mkt_coord_str_1 = "equity_index_snp500_spot.bla@yahoo"
    mkt_coord_str_1 = "equity_index_snp500_spot.bla"
    match1 = re.match(parser_regex, mkt_coord_str_1).groups()

    mkt_c2 = MktCoord("equity", "stock", "cash", ("a", "b"))
