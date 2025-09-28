"""neuropacehdf5_create_example.py
Create an HDF5 file that contains data for NeuroPace EEG data.
"""
# Imports #
# Standard Libraries #
import os
import pathlib

# Third-Party Packages #

# Local Packages #
from neuropacetools.neuropacehdf5.fileobjects import NEUROPACEHDF5
from neuropacetools import neuropaceraw

# Get the latest class version
NEUROPACEHDF5_latest = NEUROPACEHDF5.get_latest_version_class()


# Main Script #
## Read the catalog data
catalog = neuropaceraw.ieegcat('./Example_ECoG_Catalog.csv')
ieeg_record = neuropaceraw.ieegget('./', catalog[-1])
print(ieeg_record)

## Create a file
# Name the Output
output_file = os.path.splitext(ieeg_record.catalog_entry.filename)[0] + ".h5"

# Construct
nph5_file = NEUROPACEHDF5_latest(file=output_file, mode="w", create=True, construct=True)

# Fill out attributes
nph5_file.attributes["start_id"] = ieeg_record.timestamps[0]
nph5_file.attributes["end_id"] = ieeg_record.timestamps[-1]
nph5_file.attributes["subject_id"] = ieeg_record.catalog_entry.initials
nph5_file.attributes["neuropace_patient_id"] = ieeg_record.catalog_entry.patient_id
nph5_file.attributes["neuropace_device_id"] = ieeg_record.catalog_entry.device_id
nph5_file.attributes["neuropace_filename_id"] = ieeg_record.catalog_entry.filename
nph5_file.attributes["neuropace_ecog_type"] = ieeg_record.catalog_entry.ecog_type
nph5_file.attributes["neuropace_ecog_trigger"] = ieeg_record.catalog_entry.ecog_trigger

nph5_file.time_axis.components["axis"].set_time_zone(ieeg_record.catalog_entry.timestamp_tz)
nph5_file.time_axis.components["axis"].sample_rate = ieeg_record.catalog_entry.sampling_rate

nph5_file.data.resize(ieeg_record.signal.shape)
nph5_file.time_axis.resize(ieeg_record.timestamps.shape)

nph5_file.data[...] = ieeg_record.signal
nph5_file.time_axis[...] = ieeg_record.timestamps

nph5_file.data.attributes["neuropace_ecog_type"] = ieeg_record.catalog_entry.ecog_type
nph5_file.data.attributes["neuropace_ecog_trigger"] = ieeg_record.catalog_entry.ecog_trigger
nph5_file.data.attributes["neuropace_ecog_trigger_timestamp"] = ieeg_record.catalog_entry.timestamp_trigger

nph5_file.flush()
nph5_file.close()
del nph5_file


# Read the file back in
loaded_file = NEUROPACEHDF5(file=output_file, mode="r")
print("\n--- File Attributes ---")
for k in loaded_file.attributes:
    print("  ", k, ": ", loaded_file.attributes[k])

print("\n--- Data Attributes ---")
for k in loaded_file.data.attributes:
    print("  ", k, ": ", loaded_file.data.attributes[k])
loaded_file.close()
