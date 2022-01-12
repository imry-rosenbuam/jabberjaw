import numpy as np
import pandas as pd
import datetime
from enum import Enum,unique
from jabberjaw.utils.mkt_classes import Singleton
from datetime import date
import holidays

class DayCountConvention(Enum):
    ACT_360=object(),      #	The 'Act/360' day count, which divides the actual number of days by 360.
    ACT_364=object(),	            #   The 'Act/364' day count, which divides the actual number of days by 364.
    ACT_365_25=object(),	        #   The 'Act/365.25' day count, which divides the actual number of days by 365.25.
    ACT_365_ACTUAL=object(),	    #   The 'Act/365 Actual' day count, which divides the actual number of days by 366 if a leap day is contained, or by 365 if not.
    ACT_365F=object(),	        #   The 'Act/365F' day count, which divides the actual number of days by 365 (fixed).
    ACT_365L=object(),	        #   The 'Act/365L' day count, which divides the actual number of days by 365 or 366.
    ACT_ACT_AFB=object(),	        #   The 'Act/Act AFB' day count, which divides the actual number of days by 366 if a leap day is contained, or by 365 if not, with additional rules for periods over one year.
    ACT_ACT_ICMA=object(),	    #   The 'Act/Act ICMA' day count, which divides the actual number of days by the actual number of days in the coupon period multiplied by the frequency.
    ACT_ACT_ISDA=object(),	    #   The 'Act/Act ISDA' day count, which divides the actual number of days in a leap year by 366 and the actual number of days in a standard year by 365.
    ACT_ACT_YEAR=object(),	    #   The 'Act/Act Year' day count, which divides the actual number of days by the number of days in the year from the start date.
    NL_360=object(),	            #   The 'NL/360' day count, which divides the actual number of days omitting leap days by 360.
    NL_365=object(),	            #   The 'NL/365' day count, which divides the actual number of days omitting leap days by 365.
    ONE_ONE=object(),	            #   The '1/1' day count, which always returns a day count of 1.
    THIRTY_360_ISDA=object(),	    #   The '30/360 ISDA' day count, which treats input day-of-month 31 specially.
    THIRTY_360_PSA=object(),	    #   The '30/360 PSA' day count, which treats input day-of-month 31 and end of February specially.
    THIRTY_E_360=object(),	    #   The '30E/360' day count, which treats input day-of-month 31 specially.
    THIRTY_E_360_ISDA=object(),	#   The '30E/360 ISDA' day count, which treats input day-of-month 31 and end of February specially.
    THIRTY_E_365=object(),	    #   The '30E/365' day count, which treats input day-of-month 31 and end of February specially.
    THIRTY_EPLUS_360=object(),	#   The '30E+/360' day count, which treats input day-of-month 31 specially.
    THIRTY_U_360=object(),	    #   The '30U/360' day count, which treats input day-of-month 31 and end of February specially.
    THIRTY_U_360_EOM=object()	#   The '30U/360 EOM' day count, which treats input day-of-month 31 and end of February specially.
    
class RollConventions(Enum):
    FOLLOWING=object(),	                    #The 'Following' convention which adjusts to the next business day.
    MODIFIED_FOLLOWING=object(),	        #he 'ModifiedFollowing' convention which adjusts to the next business day without crossing month end.
    #MODIFIED_FOLLOWING_BI_MONTHLY=object(),	#The 'ModifiedFollowingBiMonthly' convention which adjusts to the next business day without crossing mid-month or month end.
    MODIFIED_PRECEDING=object(),	        #The 'ModifiedPreceding' convention which adjusts to the previous business day without crossing month start.
    NEAREST=object(),	                    #The 'Nearest' convention which adjusts Sunday and Monday forward, and other days backward.
    NO_ADJUST=object(),	                    #The 'NoAdjust' convention which makes no adjustment.
    PRECEDING=object()	                    #The 'Preceding' convention which adjusts to the previous business day.


class HolidayCalenadr(Singleton):
    def __init__(self,dcc: DayCountConvention = DayCountConvention.ACT_ACT_ISDA, roll: RollConventions=RollConventions.NO_ADJUST,country: str ="USA"):
        self.dcc = dcc
        self.roll = roll
        self.cal = holidays.CountryHoliday(country)
    
    def date_roll(self,dt:datetime.date) -> datetime.date:
        """rolls the date according to rolling convention of the calendar

        Args:
            dt (datetime.date): the date to be rolled

        Returns:
            datetime.date: the rolled date
        """
        if dt not in self.cal:
            return dt
        
        match self.roll:
            case RollConventions.NO_ADJUST:
                return dt
            case RollConventions.FOLLOWING:
                return self.next_business_day(dt,1)
            case RollConventions.PRECEDING:
                return self.next_business_day(dt,1,False)
            case RollConventions.NEAREST:
                if dt.weekday in [5,6]:
                    return self.next_business_day(dt,1)
                else:
                    return self.next_business_day(dt,1,False)
            case RollConventions.MODIFIED_FOLLOWING:
                follow = self.next_business_day(dt,1)
                if follow.month > dt.month:
                    return self.next_business_day(dt,1,False)
                else:
                    follow
            case RollConventions.MODIFIED_PRECEDING:
                preceding = self.next_business_day(dt,1,False)
                if preceding.month != dt.month:
                    return self.next_business_day(dt,1)
                else:
                    return preceding

    def settle_date(self, dt:datetime,business_days) -> datetime.datetime:
        """returns the settlement date given the settle lag

        Args:
            dt (datetime): transaction date
            business_days ([type]): days to roll

        Returns:
            datetime.datetime: returns the settlement date
        """
        settle_date = self.next_business_day(dt,business_days)
        return self.roll(settle_date)        
    
    def next_business_day(self,start_date:datetime.date,business_days:int, direction: bool = True) -> datetime.date:
        """Generates the next business day

        Args:
            start_date (datetime.date): the benchmark date relative to which we will generate the business day
            business_days (int): how many days in the future(past) to go
            direction (bool, optional): if True does next days else does previous. Defaults to True.

        Returns:
            datetime.date: return the business day using the inherhent holiday clanendar
        """
        one_day:datetime.timedelta = datetime.timedelta(days=1) if direction else datetime.timedelta(days=-1)
        temp_day:datetime.date = start_date
        for i in range(business_days):
            next_day= temp_day + one_day
            # notice that will only work on countries with normal weekend( sat, sun)
            # TODO: create a custom rule for countries like israel
            while next_day in self.cal or next_day.weekday in [5,6]:
                next_day += one_day
            temp_day = next_day
            
        return temp_day

    def daycount(self,start:datetime.date,end:datetime.date) -> float:
        """returns the daycount according to the calendar conventions

        Args:
            start (datetime.date): start date
            end (datetime.date): end date

        Returns:
            float: time that elapsed between start and end according to the calendar conventions
        """
        
        return 1
    
if __name__ == "__main__":
    print("Le Fin")