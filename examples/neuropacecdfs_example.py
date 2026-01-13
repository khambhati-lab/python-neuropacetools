"""neuropacecdfs_example.py
Create an HDF5 file that contains data for NeuroPace EEG data.
"""
# Imports #
# Standard Libraries #
import os
import pathlib

# Third-Party Packages #

# Local Packages #
from neuropacetools import neuropaceraw
from neuropacetools.neuropacecdfs import NEUROPACECDFS
from neuropacetools.neuropacecdfs.blocks import NEUROPACECDFSContentsUpdater

# Main Script #
# Create a CDFS object
np_cdfs = NEUROPACECDFS(path="./", create=True, build=True, construct=True)

## Create a HDF5 Writer
np_cdfs_hdf5writer_block = np_cdfs.components["contents"].create_data_writer()
## Create a CDFS Contents Updater
np_cdfs_contentsupdater_block = np_cdfs.components["contents"].create_contents_updater(
        will_proxy=False, init_setup=True)


## Read the most recent catalog record entry
catalog = neuropaceraw.ieegcat('./Example_ECoG_Catalog.csv')
ieeg_record = neuropaceraw.ieegget('./', catalog[-1])
print(ieeg_record)

## Convert the catalog entry to an hdf5 file
output_file = os.path.splitext(ieeg_record.catalog_entry.filename)[0] + ".h5"
np_cdfs_hdf5writer_block.evaluate(
    ieeg_record,
    output_file,
    file_remake=False,
    slice_=[None]
)

## Update the cdfs contents with the new record
"""
np_cdfs_contentsupdater_block.evaluate(
        'start_id': 0,
        'end_id': 10,
        'start': 0,
        'end': 10,
        'tz_offset': 23,
        'sample_rate': 250.0,
        'path': './',
        'axis': 0,
        'shape': (10, 4),
        'update_id': 1,
        'id': 1
        },
    key="id",
    begin=True
)
"""
print(np_cdfs.components["contents"].data_file_type)
