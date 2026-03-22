import logging
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from jabberjaw.utils.calendars import HolidayCalenadr, CalendarConventions
from datetime import date
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class BaseInterpolator(ABC):
    ref_date: date
    cal_conv: CalendarConventions = field(default_factory=CalendarConventions)


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
    knots: List[date] = field(default_factory=list)

    def x(self, dt: date) -> float:
        i = 0
        dt0 = self.ref_date

        while dt > self.knots[i]:
            dt0 = self.knots[i]
            i += 1

        return HolidayCalenadr.daycount(self.cal_conv, dt0, dt) / HolidayCalenadr.daycount(self.cal_conv, dt0, self.knots[i]), i

    @abstractmethod
    def ifr(self, t: float) -> float:
        pass

    @abstractmethod
    def int_ifr(self, t: float) -> float:
        pass


@dataclass
class CubicSplineInterpolator(RateInterpolator):
    coffs: List[PolinomialSegment] = field(default_factory=list)

    def ifr(self, dt: date) -> float:
        raise NotImplementedError("CubicSplineInterpolator.ifr() is not yet implemented")

    def int_ifr(self, dt: date) -> float:
        raise NotImplementedError("CubicSplineInterpolator.int_ifr() is not yet implemented")

    def cubic_interp(self, dt0: date, dt1: date, dt: date, coff: PolinomialSegment) -> float:
        raise NotImplementedError("CubicSplineInterpolator.cubic_interp() is not yet implemented")

    def __post_init__(self):
        for _ in range(len(self.knots)):
            self.coffs.append(PolinomialSegment())


if __name__ == "__main__":
    print("Le Fin")
