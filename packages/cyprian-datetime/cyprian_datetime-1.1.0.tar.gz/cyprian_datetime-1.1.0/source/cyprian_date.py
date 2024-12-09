"""
This code defines a class which holds a Cyprian date.
"""

# Standard imports.
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Self

# Non-standard imports.
import ephem

# Local imports.
from . import constants

##############
# MAIN CLASS #
##############

@dataclass
class CyprianDate:
    """ The class in question. """
    year: int
    month: int
    day: int

    def __str__(self) -> str:
        month_name = constants.MONTH_NAMES[self.month]
        month_str = month_name[:3]
        day_str = str(self.day)
        if len(day_str) == 1:
            day_str = "0"+day_str
        year_str = f"{constants.YEAR_INITIAL}{self.year}"
        result = f"{day_str} {month_str} {year_str}"
        return result

    def advance_one_day(self, current_greg: datetime):
        """ Find the next day in the calendar. """
        if new_moon_tomorrow(current_greg):
            self.advance_one_month(current_greg)
        else:
            self.day += 1

    def advance_one_month(self, current_greg: datetime):
        """ Ronseal. """
        if self.month == constants.LEAP_MONTH:
            self.advance_one_year()
        elif (
            self.month == constants.LAST_MONTH and
            tomorrow_is_on_or_after_vernal_equinox(current_greg)
        ):
            self.advance_one_year()
        else:
            assert self.month <= constants.LAST_MONTH
            self.month += 1
            self.day = 1

    def advance_one_year(self):
        """ Ronseal. """
        self.year += 1
        self.month = 1
        self.day = 1

    @classmethod
    def from_str(cls, init_str: str) -> Self:
        """
        Create an instance of this class from a string.
        Expected format is DD MMM TY.
        """
        day_str = init_str[0:2]
        month_str = init_str[3:6]
        year_str = init_str[7:]
        init_day = int(day_str)
        init_month = constants.MONTH_NAMES.index(month_str)
        init_year = int(year_str[1:])
        result = cls(init_day, init_month, init_year)
        return result

####################
# HELPER FUNCTIONS #
####################

def new_moon_tomorrow(greg: datetime) -> bool:
    """ Determine whether the new moon occurs tomorrow. """
    next_new_moon = get_next_new_moon(greg)
    tomorrow = greg+timedelta(days=1)
    return fall_on_same_day(next_new_moon, tomorrow)

def get_next_new_moon(greg: datetime) -> datetime:
    """ Get the Gregorian datetime for the next new moon. """
    ephem_date = ephem.next_new_moon(greg)
    result = to_datetime(ephem_date)
    return result

def to_datetime(ephem_date: ephem.Date) -> datetime:
    """ Convert an ephem date object into a timezone-aware datetime object. """
    result = ephem_date.datetime()
    result = result.replace(tzinfo=timezone.utc)
    return result

def fall_on_same_day(left: datetime, right: datetime) -> bool:
    """ Determine whether two events occur on the same calendar day. """
    if round_down_to_nearest_day(left) == round_down_to_nearest_day(right):
        return True
    return False

def round_down_to_nearest_day(greg: datetime) -> datetime:
    """ Ronseal. """
    result = datetime(greg.year, greg.month, greg.day, tzinfo=timezone.utc)
    return result

def get_vernal_equinox(year: int) -> datetime:
    """ Ronseal. """
    ephem_date = ephem.next_vernal_equinox(str(year))
    result = to_datetime(ephem_date)
    return result

def tomorrow_is_on_or_after_vernal_equinox(greg: datetime) -> bool:
    """ Ronseal. """
    tomorrow = greg+timedelta(days=1)
    rounded_equinox = round_down_to_nearest_day(get_vernal_equinox(greg.year))
    if tomorrow >= rounded_equinox:
        return True
    return False

def get_cyprian_new_year(year: int) -> datetime:
    """
    Given the Gregorian year, calculate the Gregorian equivalent of the Cyprian
    New Year falling within that calendar year.
    """
    ephem_date = ephem.next_new_moon(get_vernal_equinox(year))
    unrounded = to_datetime(ephem_date)
    result = round_down_to_nearest_day(unrounded)
    return result

def get_cyprian_year_beginning_with_greg_year(greg_year: int) -> int:
    """ Get the Cyprian year which begins with the given Gregorian year. """
    result = greg_year-constants.CYPRIAN_GREGORIAN_YEAR_DIFF
    return result

def get_greg_year_ending_with_cyprian_year(cyprian_year: int) -> int:
    """ Get the Gregorian year which ends with the given Cyprian year. """
    result = cyprian_year+constants.CYPRIAN_GREGORIAN_YEAR_DIFF
    return result
