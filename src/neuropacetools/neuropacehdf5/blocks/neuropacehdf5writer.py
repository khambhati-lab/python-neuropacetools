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
from ..neuropacehdf5 import NEUROPACEHDF5


# Definitions #
# Classes #
