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

# Local Packages #
from .ieegcat import CatalogEntry


# Definitions #
# Classes #
class IEEGRecord(NamedTuple):
    signal: np.array
    timestamps: np.array
    channels: np.array
    catalog_entry: CatalogEntry
