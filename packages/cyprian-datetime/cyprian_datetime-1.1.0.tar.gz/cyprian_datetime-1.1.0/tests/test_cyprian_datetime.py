"""
This code tests the Concordance class.
"""

# Standard imports.
from datetime import timedelta, timezone

# Local imports.
from source.cyprian_date import CyprianDate
from source.cyprian_datetime import CyprianDateTime

#########
# TESTS #
#########

def test_cyprian_datetime_create():
    """ Test that creating an instance of the class works as intended. """
    greg_year = 2024
    greg_month = 1
    greg_day = 1
    cyprian_date = CyprianDate(10, 10, 21)
    cyprian_datetime = \
        CyprianDateTime(greg_year, greg_month, greg_day, tzinfo=timezone.utc)
    assert cyprian_datetime.year == greg_year
    assert cyprian_datetime.month == greg_month
    assert cyprian_datetime.day == greg_day
    assert cyprian_datetime.cyprian == cyprian_date

def test_cyprian_datetime_sync():
    """ Test that the Cyprian date is updated with the Gregorian date. """
    cyprian_datetime = CyprianDateTime(2024, 1, 1, tzinfo=timezone.utc)
    today_cyprian_date = CyprianDate(10, 10, 21)
    tomorrow_cyprian_date = CyprianDate(10, 10, 22)
    assert cyprian_datetime.cyprian == today_cyprian_date
    cyprian_datetime += timedelta(days=1)
    assert cyprian_datetime.cyprian == tomorrow_cyprian_date

def test_cyprian_datetime_from_cyprian_str():
    """
    Test that, when we initialise a CyprianDateTime object from a string
    representation of a Cyprian date, it behaves as expected.
    """
    cyprian_datetime = CyprianDateTime.from_cyprian_str("01-Pri-T1")
    assert cyprian_datetime.year == 2014
    assert cyprian_datetime.month == 3
    assert cyprian_datetime.day == 30

def test_cyprian_datetime_to_dict():
    """ Test that the correct dict is created. """
    cyprian_datetime = CyprianDateTime(2024, 1, 1, tzinfo=timezone.utc)
    actual = cyprian_datetime.to_dict()
    assert actual["cyprian"]["year"] == 10
    assert actual["cyprian"]["month"] == 10
    assert actual["cyprian"]["day"] == 21
    assert actual["gregorian"] == "2024-01-01 00:00:00+00:00"

def test_cyprian_datetime_to_json():
    """ Test that the correct JSON string is created. """
    cyprian_datetime = CyprianDateTime(2024, 1, 1, tzinfo=timezone.utc)
    actual = cyprian_datetime.to_json()
    expected = (
        '{"gregorian": "2024-01-01 00:00:00+00:00", '+
        '"cyprian": {"year": 10, "month": 10, "day": 21, '+
        '"string": "21 Dec T10"}}'
    )
    assert actual == expected
