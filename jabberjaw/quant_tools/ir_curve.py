from mimetypes import init
import numpy as np
import pandas as pd
from datetime import datetime,date
from dataclasses import dataclass,field
from abc import ABC, abstractmethod
from enum import Enum
from sqlalchemy import false
from jabberjaw.utils.calendars import DayCountConvention  

@dataclass
class Interpolator(ABC):
    
    @abstractmethod
    def rate(dt1:date,dt2:date,dcc:DayCountConvention) -> float:
        return 1

@dataclass
class BaseCurve:
    _dcc: DayCountConvention
    ref_date:date


@dataclass
class Curve(BaseCurve):
    
    interpolator: Interpolator 
    
    def get_knots(self) -> list:
        return self.interpolator.knots
    
    def _rate(self, dt1:date, dt2:date) -> float:
        return self.interpolator.rate(dt1,dt2,self.dcc)
            
    def discount_factor(self,discount_date:date) -> float:
        return np.exp(-1 * self._rate(self.ref_date,discount_date))
    
    def forward_rate(self, forward_date:date,end_date:date) -> float:
        return 1

@dataclass
class BaseSegment(ABC):
    pass
     
@dataclass     
class RateSegment(BaseSegment):
    t0: float
    t1: float

    @abstractmethod
    def ifr(self, t: float) -> float:
        pass
    
    @abstractmethod
    def int_ifr(self,t:float) -> float:
        pass
    def x(self, t: float) -> float:
     return min(self.t1, max(self.t0,t)) - self.t0
    
class FlatRateSegment(RateSegment):
    a: float
    
    def ifr(self, t: float) -> float:
        x = self.x(t)
        return self.a if x <= self.t1 and x >= self.t0 else 0

    def int_ifr(self, t:float) -> float:
        return x * self.a
    
class LinearRateSegment(RateSegment):
    a: float
    b: float

    def ifr(self, t: float) -> float:
        x = self.x(t)
        return x * (self.b - self.a)/(self.t1 - self.t0) if x <= self.t1 and x >= self.t0 else 0
    
    def int_ifrrate(self, t: float) -> float:
        x = self.x(t)
        return x * (self.a + 0.5 * self.b * x)

class QuadraticSplineRateSegment(RateSegment):
    a: float
    b: float
    c: float
    
    def ifr(self, t: float) -> float:
        x = self.x(t)
        return self.a + x * (self.b + x * self.c) if x >= self.t0 and x <= self.t1 else 0
    
    def int_ifr(self, t: float) -> float:
        x = min(self.t1,max(self.t0,t)) - self.t0
        return x * (self.a + x * (0.5 * self.b + x * (1/3 * self.c)))
     
class CubicSplineRateSegment(RateSegment):
    a: float
    b: float
    c: float
    d: float
    
    def ifr(self, t: float) -> float:
        x = self.x(t)
        return self.a + x * (self.b + x * (self.c + x * self.d)) if x >= self.t0 and x <= self.t1 else 0
    
    def int_ifr(self, t: float) -> float:
        x = self.x(t)
        return x * (self.a + x * (0.5 * self.b + x * (1/3 * self.c + x * (1/4 * self.d))))

if __name__ == "__main__":
    
    x = BaseCurve(DayCountConvention.ACT_360,date(year=2020,month=11,day=14))
    print("Hello Buddy")