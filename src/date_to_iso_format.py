# date_to_iso_format.py

import warnings
from datetime import datetime
import pytz

warnings.simplefilter(action='ignore', category=FutureWarning)


def init():
    pass


def validate_iso_format(date_text):
    try:
        # Try parsing the date string to see if it's in the correct format
        datetime.fromisoformat(date_text)
        return True
    except ValueError:
        return False


def convert_to_iso_format(schedule_start, schedule_end, time_zone):
    # Validate the date format before proceeding
    if not validate_iso_format(schedule_start) or not validate_iso_format(schedule_end):
        raise ValueError("Invalid date or time format. Please use the correct format (YYYY-MM-DDTHH:MM).")

    # Convert the input times to datetime objects
    start_dt = datetime.fromisoformat(schedule_start)
    end_dt = datetime.fromisoformat(schedule_end)

    # Check if the end time is earlier than the start time
    if end_dt < start_dt:
        raise ValueError("End Date/Time cannot be earlier than Start Date/Time.")

    # Localize the datetime objects to the selected time zone
    tz = pytz.timezone(time_zone)
    start_dt = tz.localize(start_dt)
    end_dt = tz.localize(end_dt)

    # Convert to ISO 8601 format
    schedule_start_iso = start_dt.isoformat()
    schedule_end_iso = end_dt.isoformat()

    return schedule_start_iso, schedule_end_iso

