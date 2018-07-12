#!/usr/bin/env python

import pandas as pd
import datetime as dt
from pandas.tseries.offsets import CustomBusinessDay as cbd
from pandas.tseries.holiday import (get_calendar, HolidayCalendarFactory,
                                    AbstractHolidayCalendar, Holiday,
                                    nearest_workday, USMemorialDay, USLaborDay,
                                    USThanksgivingDay, GoodFriday, USPresidentsDay,
                                    USMartinLutherKingJr)

class operating_time(object):
    
    def __init__(self, bt_start=9, bt_close=17, exclusion_list=[]):
        self.bt_start = bt_start
        self.bt_close = bt_close
        self.bt_len = self.bt_close - self.bt_start
        self.exclusion = []
        self.holidays = [
            Holiday('NewYearsDay', month=1, day=1, observance=nearest_workday),
            USMartinLutherKingJr,
            USPresidentsDay,
            GoodFriday,
            USMemorialDay,
            Holiday('USIndependenceDay', month=7, day=4, observance=nearest_workday),
            USLaborDay,
            USThanksgivingDay,
            Holiday('Christmas', month=12, day=25, observance=nearest_workday)]

        class CustomCal(AbstractHolidayCalendar):
            rules = self.holidays

        self.cal = get_calendar('CustomCal')
        self.bday = cbd(calendar=self.cal)

        
    def list_holidays(self,as_string=False):
        holiday_name_list = [i.name for i in self.holidays]
        if as_string:
            for e, i in enumerate(holiday_name_list):
                print '{0}. {1}'.format(e,i)
        return holiday_name_list

    
    def remove_holidays(self,exclusion_list=[]):
        for i in exclusion_list:
            self.exclusion.append(i)
        holiday_list = []
        for i in self.holidays:
            if i.name not in self.exclusion:
                holiday_list.append(i)
        self.holidays = holiday_list
        class CustomCal(AbstractHolidayCalendar):
            rules = self.holidays
        self.cal = get_calendar('CustomCal')
        self.bday = cbd(calendar=self.cal)

    
    def list_us_bd(self,x, y):
        return pd.DatetimeIndex(start=x.date(), end=y.date(), freq=self.bday)


    def count_bdays(self, x, y):
        try:
            val = len(pd.DatetimeIndex(start=x.date(), end=y.date(), freq=self.bday))
            return val
        except:
            return None

    
    def is_bday(self,x):
        if self.count_bdays(x, x) == 1:
            return True
        else:
            return False

    
    def hr_in(self, x):
        hrIn = 0
        if self.is_bday(x) and x.hour >= self.bt_start:
            if x.hour >= self.bt_close:
                hrIn = self.bt_len
            else:
                hrIn = (x.hour * 3600 + x.minute * 60 + x.second) / 3600.0 - self.bt_start
        return hrIn


    def hr_out(self, x):
        hrOut = 0
        if self.is_bday(x) and x.hour < self.bt_close:
            if x.hour < self.bt_start:
                hrOut = self.bt_len
            else:
                hrOut = self.bt_len - self.hr_in(x)
        return hrOut


    def bdays(self, a, b):
        try:
            if pd.isnull(a) or pd.isnull(b):
                return None
            if a > b:
                x, y = b, a
            else:
                x, y = a, b
            bd_val = self.count_bdays(x, y)
            bds = bd_val - (self.hr_in(x) + self.hr_out(y)) / float(self.bt_len)
            if a > b:
                bds = 0 - bds
            return bds
        except:
            return None
        

    def btime(self, a, b):
        try:
            val = self.us_bdays(a,b)
            val = dt.timedelta(days=int(val),hours=(val-int(val))*self.bt_len)
            return val
        except:
            return None
