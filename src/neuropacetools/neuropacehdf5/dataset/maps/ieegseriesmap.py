"""neuraltimeseriesmap.py
Defines neural time series data.
"""
# Package Header #
from ....header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections.abc import Mapping
from typing import Any

# Third-Party Packages #
from hdf5objects.dataset.maps import ElectricalSeriesMap
from hdf5objects.dataset.axes import TimeAxisMap
from hdf5objects.dataset.axes import LabelAxisMap
from hdf5objects.dataset.components import TimeSeriesComponent


# Definitions #
# Classes #
class IEEGSeriesMap(ElectricalSeriesMap):
    """A base outline which defines a neural time series and its methods."""

    default_attribute_names: Mapping[str, str] = ElectricalSeriesMap.default_attribute_names | {
        "units": "units",
        "neuropace_ecog_type": "neuropace_ecog_type",
        "neuropace_ecog_trigger": "neuropace_ecog_trigger",
        "neuropace_ecog_trigger_timestamp": "neuropace_ecog_trigger_timestamp"
    }
    default_attributes: Mapping[str, Any] = ElectricalSeriesMap.default_attributes | {
            "units": "digital_counts",
            "neuropace_ecog_type": "",
            "neuropace_ecog_trigger": "",
            "neuropace_ecog_trigger_timestamp": 0}
    
    default_axis_maps: list[dict[str, Any], ...] = ElectricalSeriesMap.default_axis_maps
    
    default_component_types: dict[str, Any] = ElectricalSeriesMap.default_component_types | {}
