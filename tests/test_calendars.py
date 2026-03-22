"""Tests for jabberjaw.utils.calendars"""
import datetime
import pytest
from jabberjaw.utils.calendars import (
    CalendarConventions,
    DayCountConvention,
    HolidayCalenadr,
)


@pytest.fixture
def act360():
    return CalendarConventions(dcc=DayCountConvention.ACT_360)


@pytest.fixture
def act365f():
    return CalendarConventions(dcc=DayCountConvention.ACT_365F)


@pytest.fixture
def act_act():
    return CalendarConventions(dcc=DayCountConvention.ACT_ACT_ISDA)


class TestDaycount:
    def test_act360_one_year(self, act360):
        start = datetime.date(2020, 1, 1)
        end = datetime.date(2021, 1, 1)
        dc = HolidayCalenadr.daycount(act360, start, end)
        assert abs(dc - 366 / 360) < 1e-9  # 2020 is a leap year

    def test_act365f_one_year(self, act365f):
        start = datetime.date(2021, 1, 1)
        end = datetime.date(2022, 1, 1)
        dc = HolidayCalenadr.daycount(act365f, start, end)
        assert abs(dc - 365 / 365) < 1e-9

    def test_act360_zero_days(self, act360):
        d = datetime.date(2021, 6, 15)
        assert HolidayCalenadr.daycount(act360, d, d) == 0.0

    def test_act_act_one_non_leap_year(self, act_act):
        start = datetime.date(2021, 1, 1)
        end = datetime.date(2022, 1, 1)
        dc = HolidayCalenadr.daycount(act_act, start, end)
        assert abs(dc - 1.0) < 1e-6

    def test_act_act_leap_year(self, act_act):
        start = datetime.date(2020, 1, 1)
        end = datetime.date(2021, 1, 1)
        dc = HolidayCalenadr.daycount(act_act, start, end)
        assert abs(dc - 1.0) < 1e-6
