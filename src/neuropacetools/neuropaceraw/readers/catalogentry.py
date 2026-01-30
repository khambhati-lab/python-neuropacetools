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
from datetime import datetime, timedelta, timezone, tzinfo
import pathlib
import re
from typing import Any
from typing import NamedTuple
from typing import Union

# Third-Party Packages #
from dspobjects.time import nanostamp

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
    timestamp_start:  nanostamp
    timestamp_trigger: nanostamp
    timestamp_tz: tzinfo

    @classmethod
    def from_csv(cls, _CatalogEntry, new_reference_timestamp=None):

        # Convert to TZ-Aware
        ts = datetime.fromisoformat(_CatalogEntry.timestamp)
        raw_utc_ts = datetime.fromisoformat(_CatalogEntry.raw_utc_timestamp)
        raw_local_ts = datetime.fromisoformat(_CatalogEntry.raw_local_timestamp)

        raw_delta = raw_utc_ts.replace(tzinfo=None) - raw_local_ts
        offset_hr = raw_delta.total_seconds() / 3600.0
        offset_td = timedelta(hours=-1*offset_hr)
        fixed_tz = timezone(offset_td)

        ts_start = nanostamp(ts.replace(tzinfo=fixed_tz))
        ts_trigger = nanostamp(raw_local_ts.replace(tzinfo=fixed_tz))

        ts_start = (ts_start - nanostamp(offset_td))
        ts_trigger = (ts_trigger - nanostamp(offset_td))

        # Date shift the timestamps based on new reference
        if new_reference_timestamp is not None:
            reref_ts = nanostamp(datetime.fromisoformat(new_reference_timestamp))
            ts_start = ts_start - reref_ts
            ts_trigger = ts_trigger - reref_ts
            
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
            fixed_tz
        )
