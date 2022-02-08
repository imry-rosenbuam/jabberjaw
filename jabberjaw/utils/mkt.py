import datetime
from dataclasses import dataclass, field
from jabberjaw.utils.mkt_classes import MktCoord
from jabberjaw.data_manager import mkt_data_manager

mkt_types = tuple(["close","live"])

@dataclass
class Mkt:
    """ mkt object representing a snapshot of the market for a given timestamp (refdate, obstime) schema"""
    ref_date: datetime.date
    _ref_date: datetime.date = field(init=False, repr=False)
    obs_time: datetime.datetime = None
    _obs_time: datetime.datetime = field(default=None,init=False,repr=False)
    _data: dict = field(default_factory=dict)

    def __hash__(self) -> int:
        return hash(self.ref_date) + hash(self.obs_time)
        
    @property
    def obs_time(self) -> datetime.datetime:
        return self._obs_time
    
    @obs_time.setter
    def obs_time(self, tm: datetime.datetime):
        self._obs_time = tm if not isinstance(tm,property) else None
    
    @property
    def ref_date(self)-> datetime.date:
        return self._ref_date
    
    @ref_date.setter
    def ref_date(self,dt:datetime.date):
        self._ref_date = dt 
        
    def get_mkt_data(self, mkt_coord: MktCoord) -> dict:
        if mkt_coord.get_mkt_tuple() not in self._data.keys():
            self.__load_mkt_data(mkt_coord)

        return self._data.get(mkt_coord.get_mkt_tuple())['Adj Close']

    def __load_mkt_data(self, mkt_coord: MktCoord) -> None:
        self._data[mkt_coord.get_mkt_tuple()] = mkt_data_manager.get_mkt_data(mkt_coord, self.ref_date,
                                                                              obs_time=self.obs_time)


if __name__ == '__main__':
    # an example on how to load mkt data for a specific date and specific dataset
    dt = datetime.date(year=2020, month=11, day=16)
    mkt = Mkt(ref_date=dt)
    mkt_c = MktCoord("equity", "single stock", "a")
    xxx = mkt.get_mkt_data(mkt_c)
    print(xxx)
    x = 1
    print('le fin')
