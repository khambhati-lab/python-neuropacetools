"""neuropacehdf5writer.py
A block which writes information to an NEUROPACEHDF5 file.
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
from datetime import datetime, tzinfo
from pathlib import Path
from typing import Any, ClassVar

# Third-Party Packages #
from blockobjects import BaseBlock
import numpy as np

# Local Packages #
from ...neuropacehdf5 import NEUROPACEHDF5
from ...neuropaceraw import IEEGRecord

# Definitions #
# Classes #
class NEUROPACEHDF5Writer(BaseBlock):
    """A block which writes information to an NEUROPACEHDF5 file.

    Class Attributes:
        default_input_names: The default ordered tuple with the names of the inputs.
        default_output_names: the default ordered tuple with the names of the outputs.
        init_setup: Determines if the setup will occur duing initialization.

    Attributes:
        file: A reference to the current NEUROPACEHDF5 file being written.
        file_path: Path for file to be written.
        file_remake: Specifies whether an existing file should be remade. 
        file_type: Specifies the latest class version for NEUROPACEHDF5 type.
    """

    # Class Atrributes #
    default_input_names: ClassVar[tuple[str, ...]] = ("ieeg_record", "file_path", "file_remake",)
    default_output_names: ClassVar[tuple[str, ...]] = ("entry",)
    init_setup: ClassVar[bool] = False

    # Attributes #
    file: NEUROPACEHDF5 | None = None
    file_type: type[NEUROPACEHDF5] = NEUROPACEHDF5.get_latest_version_class()
    file_path: Path = None
    file_remake: bool = False

    current_ieeg_record: IEEGRecord = None


    # Magic Methods #
    # Construction/Deconstruction
    def __init__(
        self,
        file: NEUROPACEHDF5 | None = None,
        file_type: type[NEUROPACEHDF5] = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #

        # Parent Attributes #
        super().__init__(init=False)

        # Construct #
        if init:
            self.construct(file, file_type, *args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        file: NEUROPACEHDF5 | None = None,
        file_type: type[NEUROPACEHDF5] = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Assign Attributes #
        if file is not None:
            self.file = file

        if file_type is not None:
            self.file_type = file_type

        # Construct Parent #
        super().construct(*args, **kwargs)

    # File
    def change_file(
        self,
        ieeg_record,
        file_path,
        file_remake,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # Close Previous File
        if self.file is not None:
            self.file.close()

        # Open File
        match file_remake:
            case True:
                Path(file_path).unlink()
                file_remake = False
            case False:
                file_remake = False

        self.file = self.file_type(**({
            "file": file_path,
            "mode": "w",
            "create": True,
            "construct": True
            })
        )

        # Fill out file-level attributes
        self.file.attributes["start_id"] = ieeg_record.timestamps[0]
        self.file.attributes["end_id"] = ieeg_record.timestamps[-1]
        self.file.attributes["subject_id"] = ieeg_record.catalog_entry.initials
        self.file.attributes["neuropace_patient_id"] = ieeg_record.catalog_entry.patient_id
        self.file.attributes["neuropace_device_id"] = ieeg_record.catalog_entry.device_id
        self.file.attributes["neuropace_filename_id"] = ieeg_record.catalog_entry.filename
        self.file.attributes["neuropace_ecog_type"] = ieeg_record.catalog_entry.ecog_type
        self.file.attributes["neuropace_ecog_trigger"] = ieeg_record.catalog_entry.ecog_trigger

        # Fill out time axis level attributes
        self.file.time_axis.components["axis"].set_time_zone(ieeg_record.catalog_entry.timestamp_tz)
        self.file.time_axis.components["axis"].sample_rate = ieeg_record.catalog_entry.sampling_rate

        # Update Stored File Kwargs
        self.file_path = None
        self.file_remake = None

        # Set Single Write Multiple Read
        self.file.swmr_mode = True

        # Clear Stored record info
        self.current_ieeg_record = None

    # Writing Methods
    def set_data_slice(
        self,
        data,
        nanostamps,
        slice_: slice,
        axis: int = 0
    ) -> None:
        # Get Dataset
        dataset = self.file.data
        time_axis = self.file.time_axis

        # Get Slicing
        file_shape = dataset.shape
        n_samples = file_shape[axis]
        data_shape = data.shape
        d_slicing = list(slice(d) for d in data_shape)
        d_slicing[axis] = slice_
        d_slicing = tuple(d_slicing)

        # Resize Data if needed
        new_time_shape = (
            n_sample if slice_ is None or slice_.stop is None else
                max(n_samples, slice_.stop),
        )
        new_data_shape = list(
            max(f, d) for f, d in zip(file_shape, data_shape)
        )
        new_data_shape[axis] = new_time_shape[0]
        if tuple(new_data_shape) != file_shape:
            dataset.resize(new_data_shape)
            if new_time_shape[0] > time_axis.shape[0]:
                time_axis.resize(new_time_shape)

        # Update Data
        time_axis[slice_] = nanostamps
        dataset[d_slicing] = data
        self.file.flush()

    def append_data(self, data, nanostamps) -> None:
        # Get File's Dataset
        dataset = self.file.data

        # Get Slicing
        d_slicing = [slice(None, i) for i in data.shape]
        d_slicing[0] = slice(dataset.shape[0], data.shape[0])
        d_slicing = tuple(d_slicing)
        n_slicing = slice(self.file.time_axis.shape[0], data.shape[0])

        # Update Data
        dataset.append(
            data[d_slicing],
            component_kwargs={
                "timeseries": {"data": nanostamps[n_slicing]}
            }
        )
        self.file.flush()


    # IO
    def build_io(
        self,
        *args: Any,
        override: bool = False,
        **kwargs: Any
    ) -> None:
        """Builds the IO with the default settings and routing.

        Args:
            *args: Positional arguments for creating the IO.
            override: Determines if the IO will be overridden.
            **kwargs: Keyword arguments for creating the IO.
        """
        # TODO: Determine if the CallbackIOWrapper should also be
        # StaticWrapper to allow method calls.
        self.inputs.io_objects["ieeg_record"].wrapped.set_maxsize(3)
        self.inputs.io_objects["file_path"].wrapped.set_maxsize(3)
        self.inputs.io_objects["file_remake"].wrapped.set_maxsize(3)

    # Setup
    def setup(
        self,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Sets up this block."""
        return None

    # Evaluate
    def evaluate(
        self,
        ieeg_record: IEEGRecord,
        file_path: Path,
        file_remake: bool,
        write_method: str = "append_data",
        *args: Any,
        **kwargs: Any
    ) -> Any:
        """Writes information to an NEUROPACEHDF5 file.


        Args:
            ieeg_record: Information to write to the file.
            file_path: Path of file to be written.
            file_remake: Remake existing file.
            write_method: Class method name to use for writing data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.


        Returns:
            An enty to insert into an NEUROPACECDFS contents table.
        """
        # change File if existing file conditions do not match
        if file_path != self.file_path:
            self.change_file(
                ieeg_record,
                file_path,
                file_remake
            )

        # Update File Info
        self.current_ieeg_record = ieeg_record

        # Write Data
        method = getattr(self, write_method)
        method(
            ieeg_record.signal,
            ieeg_record.timestamps
        )

        # Return File Info
        return ieeg_record

    # Teardown
    async def teardown(
        self,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Tears down this block."""
        if self.file is not None:
            self.file.close()

        await self.outputs.put_item_async(
            self.signal_io_name,
            {"done_flag": True}
        )
