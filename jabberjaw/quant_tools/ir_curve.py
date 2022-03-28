import numpy as np
import pandas as pd
from datetime import datetime,date
from dataclasses import dataclass
from abc import ABC, abstractmethod
from jabberjaw.utils.calendars import DayCountConvention  

@dataclass
class Interpolator(ABC):
    knots: list
    polinomials: list
    
    @abstractmethod
    def rate(dt1:date,dt2:date,dcc:DayCountConvention) -> float:
        return 1

@dataclass
class Curve:
    dcc: DayCountConvention
    ref_date:date 
    interpolator: Interpolator 
    
    def get_knots(self) -> list:
        return self.interpolator.knots
    
    def _rate(self, dt1:date, dt2:date) -> float:
        return self.interpolator.rate(dt1,dt2,self.dcc)
            
    def discount_factor(self,discount_date:date) -> float:
        return np.exp(-1 * self._rate(self.ref_date,discount_date))
    
    def forward_rate(self, forward_date:date,end_date:date) -> float:
        
        return 1


if __name__ == "__main__":
    
    
    print("Hello Buddy")