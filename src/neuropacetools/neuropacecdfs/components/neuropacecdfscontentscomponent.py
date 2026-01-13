""" neuropacecdfscontentscomponent.py

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
from typing import Any

# Third-Party Packages #
from cdfs.components import CDFSTimeContentsComponent
from dspobjects.time import Timestamp
import numpy as np
from sqlalchemy.orm import Session

# Local Packages #
from ...neuropacehdf5 import NEUROPACEHDF5, NEUROPACEHDF5Writer
from ..arrays import NEUROPACEContentsProxy
from ..blocks import NEUROPACECDFSContentsUpdater


# Definitions #
# Classes #
class NEUROPACECDFSContentsComponent(CDFSTimeContentsComponent):
    # Attributes #
    date_format: str = "%d"
    time_format: str = "%H~%M~%S"

    data_file_type: type[NEUROPACEHDF5] = NEUROPACEHDF5.get_latest_version_class()
    proxy_type: type[NEUROPACEContentsProxy] = NEUROPACEContentsProxy

    # Instance Methods #
    # Contents and Files
    def correct_contents(
        self,
        path: Path | None = None,
        session: Session | None = None,
        begin: bool = False,
    ) -> None:
        """Corrects the contents of the file.

        Args:
            path: The path to the file.
            session: The SQLAlchemy session to apply the modification. Defaults to None.
            begin: If True, begins a transaction for the operation. Defaults to False.
        """
        if path is None:
            path = self._composite().path
        print(path, session, begin)
        self.contents_table.correct_contents(session=session, path=path, begin=begin)

    def generate_file_path(self, filename):
        composite = self._composite()

        task_name = "task-clips"
        task_path = composite.path / task_name
        task_path.mkdir(exist_ok=True)

        file_name = f"{filename}.h5"

        return task_path / file_name, Path(f"{task_name}/{file_name}")

    def format_entry(
        self,  
        filename: str
    ) -> dict:
        full_path, rel_path = self.generate_file_path(filename)
        file = self.data_file_type(full_path)
        return {
            "path": rel_path,
            "shape": file.data.shape, 
            "axis": file.time_axis.components["axis"].axis,
            "start": file.start_datetime,
            "end": file.end_datetime,
            "sample_rate": file.sample_rate,
            "tz_offset": int(file.time_axis.components["axis"].tzinfo.utcoffset(None).total_seconds()),
            "start_id": int(file.attributes["start_id"]),
            "end_id": int(file.attributes["end_id"]),
            "neuropace_device_id": int(file.attributes["neuropace_device_id"]),
            "neuropace_ecog_trigger_timestamp": int(file.data.attributes["neuropace_ecog_trigger_timestamp"]),
            "neuropace_ecog_trigger": file.data.attributes["neuropace_ecog_trigger"],
            "neuropace_ecog_type": file.data.attributes["neuropace_ecog_type"]
        }

    def create_data_writer(self, **kwargs) -> NEUROPACEHDF5Writer:
        return NEUROPACEHDF5Writer(file_type=self.data_file_type, **kwargs)

    def create_contents_updater(self, **kwargs) -> NEUROPACECDFSContentsUpdater:
        return NEUROPACECDFSContentsUpdater(cdfs=self.composite, **kwargs)
