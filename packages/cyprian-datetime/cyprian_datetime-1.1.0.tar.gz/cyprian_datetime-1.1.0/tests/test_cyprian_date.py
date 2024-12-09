"""
This code tests the CyprianDate class and its helper functions.
"""

# Standard imports.
from datetime import datetime, timezone

# Local imports.
from source.cyprian_date import (
    CyprianDate,
    new_moon_tomorrow,
    get_next_new_moon,
    fall_on_same_day,
    round_down_to_nearest_day,
    get_vernal_equinox,
    tomorrow_is_on_or_after_vernal_equinox,
    get_cyprian_new_year,
    get_cyprian_year_beginning_with_greg_year,
    get_greg_year_ending_with_cyprian_year
)

#########
# TESTS #
#########

def test_cyprian_date():
    """ Test that the class works as intended. """
    cyprian = CyprianDate(11, 1, 1)
    greg = datetime(2024, 4, 8, tzinfo=timezone.utc)
    assert str(cyprian) == "01 Pri T11"
    cyprian.advance_one_day(greg)
    assert str(cyprian) == "02 Pri T11"
    cyprian = CyprianDate(11, 1, 30)
    greg = datetime(2024, 5, 7, tzinfo=timezone.utc)
    cyprian.advance_one_day(greg)
    assert str(cyprian) == "01 Sec T11"
    cyprian = CyprianDate(11, 12, 29)
    greg = datetime(2025, 3, 28, tzinfo=timezone.utc)
    cyprian.advance_one_day(greg)
    assert str(cyprian) == "01 Pri T12"
    cyprian = CyprianDate(10, 12, 30)
    greg = datetime(2024, 3, 9, tzinfo=timezone.utc)
    cyprian.advance_one_day(greg)
    assert str(cyprian) == "01 Int T10"
    cyprian = CyprianDate(10, 13, 29)
    greg = datetime(2024, 4, 7, tzinfo=timezone.utc)
    cyprian.advance_one_day(greg)
    assert str(cyprian) == "01 Pri T11"

def test_new_moon_tomorrow():
    """ Test that the function returns the right output. """
    assert new_moon_tomorrow(datetime(2024, 10, 31, tzinfo=timezone.utc))
    assert not new_moon_tomorrow(datetime(2024, 10, 15, tzinfo=timezone.utc))

def test_get_next_new_moon():
    """ Test that the function returns the right output. """
    greg = datetime(2024, 10, 30, tzinfo=timezone.utc)
    nnm = get_next_new_moon(greg)
    assert nnm.year == 2024 and nnm.month == 11 and nnm.day == 1

def test_fall_on_same_day():
    """ Test that the function returns the right output. """
    left = datetime(2001, 1, 1, 1, 0, tzinfo=timezone.utc)
    right = datetime(2001, 1, 1, 2, 0, tzinfo=timezone.utc)
    wrong = datetime(2001, 1, 2, 1, 0, tzinfo=timezone.utc)
    assert fall_on_same_day(left, right)
    assert not fall_on_same_day(right, wrong)

def test_round_down_to_nearest_day():
    """ Test that the function returns the right output. """
    unrounded = datetime(2001, 1, 1, 23, 0, tzinfo=timezone.utc)
    rounded = datetime(2001, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert round_down_to_nearest_day(unrounded) == rounded

def test_get_vernal_equinox():
    """ Test that the function returns the right output. """
    equ = get_vernal_equinox(2024)
    assert equ.year == 2024 and equ.month == 3 and equ.day == 20

def test_tomorrow_is_on_or_after_vernal_equinox():
    """ Test that the function returns the right output. """
    before = datetime(2024, 1, 1, tzinfo=timezone.utc)
    on = datetime(2024, 3, 19, tzinfo=timezone.utc)
    after = datetime(2024, 4, 1, tzinfo=timezone.utc)
    assert not tomorrow_is_on_or_after_vernal_equinox(before)
    assert tomorrow_is_on_or_after_vernal_equinox(on)
    assert tomorrow_is_on_or_after_vernal_equinox(after)

def test_get_cyprian_new_year():
    """ Test that the function returns the right output. """
    actual = get_cyprian_new_year(2024)
    expected = datetime(2024, 4, 8, tzinfo=timezone.utc)
    assert actual == expected

def test_get_cyprian_year_beginning_with_greg_year():
    """ Test that the function returns the right output. """
    assert get_cyprian_year_beginning_with_greg_year(2024) == 11

def test_get_greg_year_ending_with_cyprian_year():
    """ Test that the function returns the right output. """
    assert get_greg_year_ending_with_cyprian_year(11) == 2024
