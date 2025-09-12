"""ieegdat.py
Read NeuroPace EEG Catalog file.
"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections import namedtuple
import csv
from datetime import datetime, timedelta, timezone
import pathlib
import re
from typing import Any
from typing import NamedTuple
from typing import Union

# Third-Party Packages #

# Local Packages #

# Definitions #
# Classes #
class CatalogEntry(NamedTuple):
    initials: str
    patient_id: int
    device_id: int
    session_folder: str
    filename: str
    ecog_type: str
    ecog_trigger: str
    ecog_length: float
    sampling_rate: float
    waveform_count: int
    ch_1_name: str
    ch_2_name: str
    ch_3_name: str
    ch_4_name: str
    ch_1_enabled: bool
    ch_2_enabled: bool
    ch_3_enabled: bool
    ch_4_enabled: bool
    timestamp_start:  datetime
    timestamp_trigger: datetime

    @classmethod
    def from_csv(cls, _CatalogEntry):

        # Convert to TZ-Aware
        ts = datetime.fromisoformat(_CatalogEntry.timestamp)
        raw_utc_ts = datetime.fromisoformat(_CatalogEntry.raw_utc_timestamp)
        raw_local_ts = datetime.fromisoformat(_CatalogEntry.raw_local_timestamp)

        raw_delta = raw_utc_ts.replace(tzinfo=None) - raw_local_ts
        offset_hr = raw_delta.total_seconds() / 3600.0
        offset_td = timedelta(hours=-1*offset_hr)
        fixed_tz = timezone(offset_td)

        ts_start = ts.replace(tzinfo=fixed_tz)
        ts_trigger = raw_local_ts.replace(tzinfo=fixed_tz)

        return cls(
            str(_CatalogEntry.initials),
            int(_CatalogEntry.patient_id),
            int(_CatalogEntry.device_id),
            str(_CatalogEntry.session_folder),
            str(_CatalogEntry.filename),
            str(_CatalogEntry.ecog_type),
            str(_CatalogEntry.ecog_trigger),
            float(_CatalogEntry.ecog_length),
            float(_CatalogEntry.sampling_rate),
            int(_CatalogEntry.waveform_count),
            str(_CatalogEntry.ch_1_name),
            str(_CatalogEntry.ch_2_name),
            str(_CatalogEntry.ch_3_name),
            str(_CatalogEntry.ch_4_name),
            bool(_CatalogEntry.ch_1_enabled),
            bool(_CatalogEntry.ch_2_enabled),
            bool(_CatalogEntry.ch_3_enabled),
            bool(_CatalogEntry.ch_4_enabled),
            ts_start,
            ts_trigger,
        )


# Functions #
def _clean_header(s: str, sub: str='_', casing: str | None='lower') -> str:
    """Ensure header strings can serve as python identifiers"""
    # Remove invalid characters
    s = re.sub('[^0-9a-zA-Z_]', sub, s)

    # Remove leading characters until we find a letter or underscore
    s = re.sub('^[^a-zA-Z_]+', '', s)
   
    if casing=='lower':
        s = s.lower()
    elif casing=='upper':
        s = s.upper()
    else:
        s = s

    return s

def ieegcat(path: str | pathlib.Path) -> list[namedtuple]:
    """Read Category CSV file.

    Args:
        path: Path to CSV file.

    Returns:
        data_records
    """

    # Load the raw binary file
    path = pathlib.Path(path)

    data_records = []
    with open(path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
       
        # Get the header
        header = next(reader)
        # Create a DataRecord namedtuple from header information
        _CatalogEntry = namedtuple('DataRecord', [_clean_header(col) for col in header])
        
        for row in reader:
            # Create a namedtuple instance from the current row
            # Ensure the number of elements in 'row' matches the namedtuple fields
            data_records.append(CatalogEntry.from_csv(_CatalogEntry(*row)))

    return data_records
