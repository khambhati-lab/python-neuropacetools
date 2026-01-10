"""neuropacecdfsasyncschema.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #

# Third-Party Packages #
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

# Local Packages #
from .tables import BaseNEUROPACEMetaInformationTableSchema, BaseNEUROPACEContentsTableSchema


# Definitions #
# Classes #
class NEUROPACECDFSAsyncSchema(AsyncAttrs, DeclarativeBase):
    pass


class NEUROPACEMetaInformationTableSchema(BaseNEUROPACEMetaInformationTableSchema, NEUROPACECDFSAsyncSchema):
    pass


class NEUROPACEContentsTableSchema(BaseNEUROPACEContentsTableSchema, NEUROPACECDFSAsyncSchema):
    pass

