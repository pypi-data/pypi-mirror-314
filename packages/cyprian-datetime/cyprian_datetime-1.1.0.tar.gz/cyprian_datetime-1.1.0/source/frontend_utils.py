"""
This code defines some frotend utility functions.
"""

# Standard imports.
from datetime import datetime

# Local imports.
from .concordance import Concordance
from .cyprian_date import CyprianDate

#############
# FUNCTIONS #
#############

def convert_date(to_convert: datetime|CyprianDate) -> datetime|CyprianDate:
    """ Convert a Gregorian date to a Cyprian one, or vice versa. """
    if isinstance(to_convert, datetime):
        return convert_greg_to_cyprian(to_convert)
    if isinstance(to_convert, CyprianDate):
        return convert_cyprian_to_greg(to_convert)
    raise ConversionError(f"Unanticipated type: {type(to_convert)}")

def convert_greg_to_cyprian(greg: datetime) -> CyprianDate:
    """ Ronseal. """
    concordance = Concordance()
    result = concordance.convert_greg(greg)
    return result

def convert_cyprian_to_greg(cyprian: datetime) -> datetime:
    """ Ronseal. """
    concordance = Concordance()
    result = concordance.convert_cyprian(cyprian)
    return result

##################
# HELPER CLASSES #
##################

class ConversionError(Exception):
    """ A custom exception. """
