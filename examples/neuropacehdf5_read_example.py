# Local Packages #
from neuropacetools.neuropacehdf5.fileobjects import NEUROPACEHDF5

## primary
loaded_file = NEUROPACEHDF5(file="example.h5", mode="r")
print(loaded_file.attributes["file_version"])
loaded_file.close()


## alternative
loaded_file = NEUROPACEHDF5(file="example2.h5", mode="r")
print(loaded_file.attributes["file_version"])
loaded_file.close()
