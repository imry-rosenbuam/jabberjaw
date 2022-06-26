from mimetypes import init
import numpy as np
import pandas as pd
from datetime import datetime,date
from dataclasses import dataclass,field
from abc import ABC, abstractmethod
from enum import Enum
from sqlalchemy import false
from jabberjaw.utils.calendars import DayCountConvention,CalendarConventions
from jabberjaw.utils.calendars import HolidayCalenadr
from typing import List, Dict, Tuple


@dataclass
class Interpolator(ABC):
    
    def rate(self, dt1:date,dt2:date,dcc:DayCountConvention) -> float:
        return 1

@dataclass
class BaseCurve(ABC):
    _cal_conven: CalendarConventions 
    ref_date:date

    @abstractmethod
    def index(self, dt: date) -> float:
        pass

@dataclass
class IRCurve(BaseCurve):
    
    interpolator: Interpolator 
    
    tenor: str = None
    
    def get_knots(self) -> list:
        return self.interpolator.knots
    
    def _rate(self, dt1:date, dt2:date) -> float:
        return self.interpolator.rate(dt1,dt2,self.dcc)
            
    def discount_factor(self,discount_date:date) -> float:
        return np.exp(-1 * self._rate(self.ref_date,discount_date))
    
    def forward_rate(self, forward_date:date,end_date:date) -> float:
        return self._rate(forward_date, end_date)/HolidayCalenadr.daycount(self._cal_conven.dcc, forward_date, end_date)





if __name__ == "__main__":
    
    x = BaseCurve(DayCountConvention.ACT_360,date(year=2020,month=11,day=14))
    print("Hello Buddy")