from dataclasses import dataclass
from abc import ABC,abstractclassmethod,abstractmethod

@dataclass
class BaseSegment(ABC):
    pass
     
@dataclass     
class RateSegment(BaseSegment):
    t0: float
    t1: float
    date0: float
    date1: float
    
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
        x = self.x(t)
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
    
    
    print("Le Fin")