import datetime
import pandas as pd
from dataclasses import dataclass, field
from jabberjaw.utils.mkt_classes import MktCoord, get_ticker, singleton, get_coord_default_source, mkt_data_cfg
import dpath.util as dpath
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
        
    def _clear_cache(self) -> None:
        self._data = dict()
        
    def get_mkt_data(self, mkt_coord: MktCoord) -> dict:
        if mkt_coord.get_mkt_tuple() not in self._data.keys():
            self.__load_mkt_data(mkt_coord)

        source = mkt_coord.source if mkt_coord.source != "default" else get_coord_default_source(mkt_coord)
        
        if source.upper() == "FRED":
            ticker = get_ticker( mkt_coord)
            val_name = ticker
        else:
            ticker = get_ticker( mkt_coord)
            val_name = 'ADJ CLOSE'
        
        return self._data.get(mkt_coord.get_mkt_tuple())[val_name]

    def __load_mkt_data(self, mkt_coord: MktCoord) -> None:
        self._data[mkt_coord.get_mkt_tuple()] = mkt_data_manager.get_mkt_data(mkt_coord, self.ref_date,
                                                                              obs_time=self.obs_time)
        
    def get_mkt_history(self, mkt_coord: MktCoord, back_date: datetime.date = datetime.date(year=1900, month = 1, day = 1)) -> pd.DataFrame:
        hist = mkt_data_manager.get_history_mkt_data(mkt_coord)
        
        if not hist.empty:
            return hist[pd.Timestamp(back_date):]
        
        return pd.DataFrame()

    def get_mkt_curve(self, ccy: str, index: str, tenor: str = None ) -> object:
        
        
        
        return object

class Mkt_Factory:
    _mkt: Mkt = None
    
    @classmethod
    def get_MKT(cls) -> Mkt:
        if cls._mkt:
            return cls._mkt
        else:
            cls._mkt = Mkt(datetime.date.today())
            return cls._mkt
        
if __name__ == '__main__':
    # an example on how to load mkt data for a specific date and specific dataset
    dt = datetime.date(year=2022, month=1, day=3)
    back_date = datetime.date(year=2019, month=11, day=16)
    mkt = Mkt(ref_date=dt)
    mkt_c = MktCoord("ir", "usd", "COM-PAPER-NONF","1M")
    mkt_c = MktCoord("fx","currency pair","USDNZD")
    xxx = mkt.get_mkt_data(mkt_c)
    print(xxx)
    #bla = mkt.get_mkt_history(mkt_c, back_date)
    x = 1
    print('le fin')
