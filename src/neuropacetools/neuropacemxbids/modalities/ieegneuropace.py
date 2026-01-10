"""IEEGNEUROPACE.py
A BIDS IEEG NEUROPACE Modality.
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
from typing import ClassVar, Any

# Third-Party Packages #
from mxbids.cdfsbids import IEEGCDFS

# Local Packages #
from .ieegneuropacecomponent import IEEGNEUROPACEComponent
#from .ieegneuropaceannotationscomponent import IEEGNEUROPACEAnnotationsComponent


# Definitions #
# Classes #
class IEEGNEUROPACE(IEEGCDFS):
    """A BIDS IEEG NEUROPACE Modality.

    Class Attributes:
        _module_: The module name for this class.
        default_component_types: Default component types for the modality.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = "neuropacetools.neuropacemxbids"
    default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
        "cdfs": (IEEGNEUROPACEComponent, {}),
        #"annotations": (IEEGNEUROPACEAnnotationsComponent, {}),
    }

