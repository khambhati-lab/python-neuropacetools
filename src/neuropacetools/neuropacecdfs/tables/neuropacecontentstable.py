""" neuropacecontentstable.py
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
from pathlib import Path
from typing import Any
from warnings import warn

# Third-Party Packages #
from cdfs import BaseTimeContentsTableSchema, TimeContentsTableManifestation
from sqlalchemy import select, lambda_stmt
from sqlalchemy.orm import Session, mapped_column
from sqlalchemy.types import BigInteger, Text

# Local Packages #
from ...neuropacehdf5 import NEUROPACEHDF5


# Definitions #
# Classes #
class BaseNEUROPACEContentsTableSchema(BaseTimeContentsTableSchema):
    """
    Columns
    -------
    
    start_id: The ID of the entry.
    end_id: The ID of the entry.
    
    path: The path of the content. Defaults to an empty string.
    axis: The axis of the content. Defaults to 0.
    shape: The shape of the content. Defaults to (0,).
    timezone: The timezone information. Defaults to None.
    start: The start time. Defaults to None.
    end: The end time. Defaults to None.
    sample_rate: The sample rate of the content. Defaults to None.
    """
    __mapper_args__ = {"polymorphic_identity": "neuropacecontents"}
    start_id = mapped_column(BigInteger, primary_key=True)
    end_id = mapped_column(BigInteger)
    neuropace_device_id = mapped_column(BigInteger)
    neuropace_ecog_trigger_timestamp = mapped_column(BigInteger)
    neuropace_ecog_trigger = mapped_column(Text)
    neuropace_ecog_type = mapped_column(Text)
    neuropace_ecog_ch1_cathode = mapped_column(Text)
    neuropace_ecog_ch1_anode = mapped_column(Text)
    neuropace_ecog_ch2_cathode = mapped_column(Text)
    neuropace_ecog_ch2_anode = mapped_column(Text)
    neuropace_ecog_ch3_cathode = mapped_column(Text)
    neuropace_ecog_ch3_anode = mapped_column(Text)
    neuropace_ecog_ch4_cathode = mapped_column(Text)
    neuropace_ecog_ch4_anode = mapped_column(Text)

    file_type: type[NEUROPACEHDF5] | None = NEUROPACEHDF5

    @classmethod
    def get_start_end_ids(cls, session: Session) -> tuple[tuple[int, int], ...]:
        statement = lambda_stmt(lambda: select(cls.start_id, cls.end_id).order_by(cls.start_id))
        return tuple(session.execute(statement))

class NEUROPACEContentsTableManifestation(TimeContentsTableManifestation):
    # Instance Methods #
    # Contents
    def get_start_end_ids(self, session: Session | None = None) -> tuple[tuple[int, int], ...]:
        if session is not None:
            return self.table_schema.get_start_end_ids(session=session)
        else:
            with self.create_session() as session:
                return self.table_schema.get_start_end_ids(session=session)
