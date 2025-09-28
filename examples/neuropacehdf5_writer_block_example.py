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
from neuropacetools.neuropacehdf5.blocks.neuropacehdf5writer import NEUROPACEHDF5Writer

# Main Script #
## Read the catalog data
catalog = neuropaceraw.ieegcat('./Example_ECoG_Catalog.csv')
ieeg_record = neuropaceraw.ieegget('./', catalog[-1])
print(ieeg_record)

## Create a file
# Name the Output
output_file = os.path.splitext(ieeg_record.catalog_entry.filename)[0] + ".h5"

# Construct
print("\n--- NEUROPACEHDF5 Writer Enabled ---")
nph5_writer = NEUROPACEHDF5Writer()
nph5_writer.evaluate(
    ieeg_record,
    output_file,
    file_remake=False,
    slice_=[None]
)
nph5_writer.teardown()
print("--- NEUROPACEHDF5 Writer Done ---")

# Read the file back in
print("\n--- NEUROPACEHDF5 Reader Enabled ---")
loaded_file = NEUROPACEHDF5(file=output_file, mode="r")
print("\n--- File Attributes ---")
for k in loaded_file.attributes:
    print("  ", k, ": ", loaded_file.attributes[k])

print("\n--- Data Attributes ---")
for k in loaded_file.data.attributes:
    print("  ", k, ": ", loaded_file.data.attributes[k])
print(loaded_file.data[...])
print(loaded_file.time_axis[...])
loaded_file.close()
print("--- NEUROPACEHDF5 Reader Done ---")

