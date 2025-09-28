# Local Packages #
from neuropacetools.neuropacehdf5.fileobjects import NEUROPACEHDF5

# Get the latest version of the versioned class to use for file writing
NEUROPACEHDF5_latest = NEUROPACEHDF5.get_latest_version_class()

## write file using latest file version
nph5_file = NEUROPACEHDF5_latest(file="example.h5", mode="w", create=True, construct=True)
print(nph5_file.attributes["file_version"])
nph5_file.close()
del nph5_file

# read file using the latest file version
loaded_file = NEUROPACEHDF5_latest(file="example.h5", mode="r")
print(loaded_file.attributes["file_version"])
loaded_file.close()
del loaded_file

# OR read file using version agnostic reader
loaded_file = NEUROPACEHDF5(file="example.h5", mode="r")
print(loaded_file.attributes["file_version"])
loaded_file.close()
del loaded_file
