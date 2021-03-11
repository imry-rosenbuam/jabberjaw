import datetime
from dataclasses import dataclass, field
from jabberjaw.mkt_utils.mkt_classes import MktCoord
from jabberjaw.data_manager import mkt_data_manager


@dataclass
class Mkt:
    """ mkt object representing a snapshot of the market for a given timestamp (refdate, obstime) schema"""
    _ref_date: datetime.date
    _obs_time: datetime.datetime = None
    _data: dict = field(default_factory=dict)

    def get_obs_time(self) -> datetime.datetime:
        return self._obs_time

    def get_ref_date(self) -> datetime.date:
        return self._ref_date

    def get_mkt_data(self, mkt_coord: MktCoord) -> dict:
        if mkt_coord.get_mkt_tuple() not in self._data.keys():
            self._load_mkt_data(mkt_coord)

        return self._data.get(mkt_coord.get_mkt_tuple())

    def _load_mkt_data(self, mkt_coord: MktCoord) -> None:
        self._data[mkt_coord.get_mkt_tuple()] = mkt_data_manager.get_mkt_data(mkt_coord, self._ref_date,
                                                                              obs_time=self._obs_time)


if __name__ == '__main__':
    pass