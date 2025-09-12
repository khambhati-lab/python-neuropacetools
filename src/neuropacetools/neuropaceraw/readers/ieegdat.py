"""ieegdat.py
Read NeuroPace EEG dat file.
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
import pathlib
from typing import Any
from typing import Union

# Third-Party Packages #
import numpy as np

# Local Packages #

# Definitions #
# Globals #
BINARY_DTYPE = np.int16
DEVICE_OFFSET = 512
BINARY_INTERLEAVE = True  # Other option is block-wise format
N_DEVICE_CHAN = 4

# Functions #
def ieegdat(
        path: str | pathlib.Path,
        n_chan: int,
        n_sample: int) -> np.array:
    """Read DAT Binary file.

    Args:
        path: Path to DAT file.
        n_chan: Number of <valid> channels in the file.
        n_sample: Number of samples per valid channel in the file.

    Returns:
        data_arr: np.ndarray (dtype: np.float) [n_sample x n_chan]
    """

    if n_chan > N_DEVICE_CHAN:
        raise Exception(f'Requesting more than {N_DEVICE_CHAN} channels.')

    # Load the raw binary file
    path = pathlib.Path(path)
    raw = np.fromfile(path, dtype=BINARY_DTYPE)

    # Check for even number of samples across channels.
    assert (len(raw) / n_chan) == (len(raw) // n_chan)
    raw_sample_per_chan = len(raw) // n_chan

    # Check number of samples expected is same as number extracted
    assert abs(raw_sample_per_chan - n_sample) <= 1
    n_sample = raw_sample_per_chan

    # Return data as reshaped numpy array
    data_arr = np.nan * np.zeros((n_sample, n_chan))
    for ii in range(n_chan):
        if BINARY_INTERLEAVE:
            data_arr[:, ii] = raw[ii::n_chan]
        else:
            data_arr[:, ii] = raw[(ii * n_sample):((ii + 1) * n_sample)]
    data_arr -= DEVICE_OFFSET

    return data_arr
