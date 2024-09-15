# date_to_iso_format.py

import warnings
from datetime import datetime
import pytz

warnings.simplefilter(action='ignore', category=FutureWarning)


def init():
    pass

def convert_to_iso_format(schedule_start, schedule_end, time_zone):

    # Convert the input times to datetime objects
    start_dt = datetime.fromisoformat(schedule_start)
    end_dt = datetime.fromisoformat(schedule_end)

    # Localize the datetime objects to the selected time zone
    tz = pytz.timezone(time_zone)
    start_dt = tz.localize(start_dt)
    end_dt = tz.localize(end_dt)

    # Convert to ISO 8601 format
    schedule_start_iso = start_dt.isoformat()
    schedule_end_iso = end_dt.isoformat()

    return schedule_start_iso, schedule_end_iso
