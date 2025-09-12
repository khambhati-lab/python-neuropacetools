"""neuropacehdf5_1.py
A HDF5 file that contains data for NeuroPace EEG data.
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

# Third-Party Packages #
from classversioning import TriNumberVersion
from classversioning import Version
from hdf5objects.hdf5bases import HDF5Map

# Local Packages #
from .neuropacehdf5 import NEUROPACEHDF5, NEUROPACEHDF5Map


# Defintions #
# Classes #
class NEUROPACEHDF5_0_1_0(NEUROPACEHDF5):
    """A HDF5 file that contains data for NEUROPACE EEG data.

    Class Attributes:
        _registration: Determines if this class will be included in class registry.
        _VERSION_TYPE: The type of versioning to use.
        FILE_TYPE: The file type name of this class.
        VERSION: The version of this class.
        default_map: The HDF5 map of this object.
    """

    VERSION: Version = TriNumberVersion(0, 1, 0)
    default_map: HDF5Map = NEUROPACEHDF5Map()
