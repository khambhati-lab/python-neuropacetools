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
from .catalogentry import CatalogEntry

# Definitions #
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

def ieegcat(path: str | pathlib.Path, new_reference_timestamp: str) -> list[namedtuple]:
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
            try:
                data_records.append(CatalogEntry.from_csv(_CatalogEntry(*row), new_reference_timestamp))
            except:
                print(f"Incorrectly formatted record, skipping: {row}")

    return data_records
