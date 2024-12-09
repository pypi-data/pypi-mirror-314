"""
This code tests the Concordance class.
"""

# Standard imports.
from datetime import datetime, timezone

# Local imports.
from source.concordance import Concordance
from source.cyprian_date import CyprianDate

#########
# TESTS #
#########

def test_cyprian_date():
    """ Test that the class works as intended. """
    greg = datetime(2024, 1, 1, tzinfo=timezone.utc)
    cyprian = CyprianDate(10, 10, 21)
    concordance = Concordance()
    actual = concordance.convert_greg(greg, force_write_first=True)
    assert actual == cyprian
    actual = concordance.convert_cyprian(cyprian, force_write_first=True)
    assert actual == greg
