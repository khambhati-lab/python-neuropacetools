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
import numpy as np
from dspobjects.time import nanostamp

# Local Packages #
from .catalogentry import CatalogEntry
from .ieegrecord import IEEGRecord
from .ieegdat import ieegdat


# Definitions #
# Functions #
def ieegget(
        path: str | pathlib.Path,
        record: CatalogEntry) -> IEEGRecord:
    """Retrieve iEEG record corresponding to catalog entry.

    Args:
        path: Path containing DAT files.
        record: A CatalogEntry corresponding to the desired file. 

    Returns:
        IEEGRecord
    """

    # Load the raw binary file
    path = pathlib.Path(path) / record.filename
    n_chan = int(record.waveform_count)
    n_sample = int(record.ecog_length * record.sampling_rate)
    data_arr = ieegdat(path, n_chan, n_sample)

    # Construct a timestamp vector
    td_vec = np.array([nanostamp(i/record.sampling_rate) for i in range(n_sample)])
    ts_arr = record.timestamp_start + td_vec

    # Construct a channel label vector
    ch_arr = np.array([
        getattr(record, f'ch_{ch_id}_name')
        for ch_id in range(1, record.waveform_count+1)
        if getattr(record, f'ch_{ch_id}_enabled')])

    return IEEGRecord(data_arr, ts_arr, ch_arr, record) 
