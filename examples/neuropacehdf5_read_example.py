# Local Packages #
from neuropacetools.neuropacehdf5.fileobjects import NEUROPACEHDF5

## primary
loaded_file = NEUROPACEHDF5(file="133940083862290000.h5", mode="r")
print(loaded_file.attributes["file_version"])
loaded_file.close()
