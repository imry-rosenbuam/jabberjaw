from dataclasses import dataclass
from abc import ABC,abstractclassmethod,abstractmethod
from jabberjaw.utils.calendars import HolidayCalenadr, CalendarConventions
from datetime import date, timedelta
from typing import Tuple, List




@dataclass
class BaseInterpolator(ABC):
    ref_date: date 
    cal_conv: CalendarConventions = CalendarConventions()

class CurveSegment(ABC):
    pass

class PolinomialSegment(CurveSegment):
    a: float = 0
    b: float = 0
    c: float = 0
    d: float = 0
     
@dataclass     
class RateInterpolator(BaseInterpolator):
    extrapolate: bool = False
    extrapolation_style: str = "flat"
    
    knots = List[date]    
    
    def x(self, dt: date) -> float:
        i = 0
        dt0 = self.ref_date
        
        #TODO: does it have to be > or >=
        while dt > self.knots[i]:
            dt0 = self.knots[i]
            i += 1
        
        return HolidayCalenadr.daycount(self.cal_conv,dt0,dt)/ HolidayCalenadr.daycount(self.cal_conv,dt0,self.knots[i]),i
    
    @abstractmethod
    def ifr(self, t: float) -> float:
        pass
    
    @abstractmethod
    def int_ifr(self,t:float) -> float:
        pass
    


     
class CubicSplineInterpolator(RateInterpolator):
    
    coffs = List[PolinomialSegment]
    
    def ifr(self, dt: date) -> float:
        x,i = self.x(dt)
        segment = self.coffs[i]
        return segment.a + x * (segment.b + x * (segment.c + x * segment.d)) if x >= self.t0 and x <= self.t1 else 0
    
    def int_ifr(self, dt: date) -> float:
        x,i = self.x(dt)
        segment = self.coffs[i]
        return x * (segment.a + x * (segment.b / 2 + x * (segment.c / 3 + x * segment.d / 4))) if x >= self.t0 and x <= self.t1 else 0
    
    def cubic_interp(self, dt0: date,dt1: date,dt:date,coff:PolinomialSegment) -> float:
        x = HolidayCalenadr.daycount(self.c)
        return x * (coff.a + x * (0.5 * coff.b + x * (1/3 * coff.c + x * (1/4 * coff.d))))
    
    def __post_init__(self):
        for i in range(len(self.knots)):
            self.coffs.append(PolinomialSegment())
    
if __name__ == "__main__":

    
    print("Le Fin")