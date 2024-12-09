"""
This code defines the extension of the standard datetime class.
"""

# Standard imports.
import json
from datetime import datetime
from typing import Self

# Local imports.
from .cyprian_date import CyprianDate
from .frontend_utils import convert_date

##############
# MAIN CLASS #
##############

class CyprianDateTime(datetime):
    """ The class in question. """
    def __new__(cls, *args, **kwargs) -> Self:
        self = super().__new__(cls, *args, **kwargs)
        self._cyprian = convert_date(self)
        return self

    def __str__(self) -> str:
        greg_str = super().__str__()
        cyprian_str = str(self.cyprian)
        result = f"{greg_str} = {cyprian_str}"
        return result

    def to_dict(self) -> dict:
        """ Get a dict representation of this object. """
        result = {
            "gregorian": super().__str__(),
            "cyprian": {
                "year": self.cyprian.year,
                "month": self.cyprian.month,
                "day": self.cyprian.day,
                "string": str(self.cyprian)
            }
        }
        return result

    def to_json(self) -> str:
        """ Get a JSON representation of this object. """
        json_obj = json.dumps(self.to_dict())
        result = str(json_obj)
        return result

    @property
    def cyprian(self) -> CyprianDate:
        """ The Cyprian equivalent to the current date. """
        self._cyprian = convert_date(self)  # Synchronise on each lookup.
        return self._cyprian

    @classmethod
    def from_cyprian(cls, cyprian: CyprianDate) -> Self:
        """ Construct an instance of this class from a CyprianDate object. """
        greg = convert_date(cyprian)
        result = cls(greg.year, greg.month, greg.day)
        return result

    @classmethod
    def from_cyprian_str(cls, cyprian_str: str) -> Self:
        """
        Construct an instance of this class from a string representation of a
        CyprianDate object.
        """
        cyprian = CyprianDate.from_str(cyprian_str)
        return cls.from_cyprian(cyprian)

####################
# HELPER FUNCTIONS #
####################

def correct_weekday(datetime_weekday: int) -> int:
    """ Adjust to system in which Sunday is the first day of the week. """
    result = (datetime_weekday+1)%7
    return result
