"""
This code tests the various frontend utility functions.
"""

# Standard imports.
from datetime import datetime, timezone

# Local imports.
from source.frontend_utils import convert_date
from source.cyprian_date import CyprianDate

#########
# TESTS #
#########

def test_convert_date():
    """ Test that the function returns the right output. """
    greg = datetime(2024, 1, 1, tzinfo=timezone.utc)
    cyprian = CyprianDate(10, 10, 21)
    actual = convert_date(greg)
    assert actual == cyprian
    actual = convert_date(cyprian)
    assert actual == greg
