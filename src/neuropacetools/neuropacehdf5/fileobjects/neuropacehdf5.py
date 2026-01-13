"""neuropacehdf5.py
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
import pathlib
from typing import Any
from typing import Union

# Third-Party Packages #
from baseobjects.functions import singlekwargdispatch
from classversioning import VersionType, Version, TriNumberVersion
import h5py
from hdf5objects.dataset import TimeAxisMap, LabelAxisMap
from hdf5objects.fileobjects import HDF5EEGMap, HDF5EEG
from hdf5objects.hdf5bases import HDF5File, HDF5Map

# Local Packages #
from ..dataset import IEEGSeriesMap

# Definitions #
# Classes #
class NEUROPACEHDF5Map(HDF5EEGMap):
    """A map for NEUROPACEHDF5 files."""
    default_attribute_names = HDF5EEGMap.default_attribute_names | {
            "start_id": "start_id",
            "end_id": "end_id",

            "neuropace_patient_id": "neuropace_patient_id",
            "neuropace_device_id": "neuropace_device_id",
            "neuropace_filename_id": "neuropace_filename_id",
            "neuropace_ecog_type": "neuropace_ecog_type",
            "neuropace_ecog_trigger": "neuropace_ecog_trigger"
    }

    default_attributes = HDF5EEGMap.default_attributes | {
            "age": "", 
            "sex": "U",
            "species": "Homo Sapien",
            
            "neuropace_patient_id": "",
            "neuropace_device_id": 0,
            "neuropace_filename_id": "",
            "neuropace_ecog_type": "",
            "neuropace_ecog_trigger": ""
    }

    default_map_names = {"data": "iEEG"}
    default_maps = {"data": IEEGSeriesMap(
        object_kwargs={
            "shape": (0, 0),
            "maxshape": (None, None),
            "compression": "gzip",
            "compression_opts": 9}
        )
    }


class NEUROPACEHDF5(HDF5EEG):
    """A HDF5 file that contains data for NeuroPace EEG data.

    Class Attributes:
        _registration: Determines if this class will be included in class registry.
        _VERSION_TYPE: The type of versioning to use.
        FILE_TYPE: The file type name of this class.
        VERSION: The version of this class.
        default_map: The HDF5 map of this object.
    """

    _registration: bool = True
    _VERSION_TYPE: VersionType = VersionType(name="NEUROPACEHDF5", class_=TriNumberVersion)
    VERSION: Version = TriNumberVersion(0, 0, 0)
    FILE_TYPE: str = "NEUROPACE_EEG"
    default_map: HDF5Map = NEUROPACEHDF5Map()

    @classmethod
    def get_version_from_file(cls, file: pathlib.Path | str | h5py.File) -> tuple[Version, h5py.File]:
        """Return a version from a file.

        Args:
            file: The path to file to get the version from.

        Returns:
            The version from the file.
        """
        v_name = cls.default_map.attribute_names["file_version"]

        if isinstance(file, pathlib.Path):
            file = file.as_posix()

        if isinstance(file, str):
            file = h5py.File(file)

        if v_name in file.attrs:
            return TriNumberVersion(file.attrs[v_name]), file
        elif cls.get_version_class(TriNumberVersion(0, 1, 0)).validate_file_type(file):
            return TriNumberVersion(0, 1, 0), file
