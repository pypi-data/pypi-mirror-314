"""
bdew_datetimes is a package that models the BDEW holiday, which is relevant for German utilities
"""

from pytz import timezone

from .calendar import create_bdew_calendar

GERMAN_TIME_ZONE = timezone("Europe/Berlin")
__all__ = ["GERMAN_TIME_ZONE", "create_bdew_calendar"]
