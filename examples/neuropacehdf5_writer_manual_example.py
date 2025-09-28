# Local Packages #
from neuropacetools.neuropacehdf5.fileobjects import NEUROPACEHDF5_0_1_0

## primary
nph5_file = NEUROPACEHDF5_0_1_0(file="example.h5", mode="w", create=True)
print(dict(nph5_file.attributes))
nph5_file.construct_file_attributes()
print(nph5_file.attributes["file_version"])
nph5_file.close()

## alternative
nph5_file = NEUROPACEHDF5_0_1_0(file="example2.h5", mode="w", create=True, construct=True)
print(nph5_file.attributes["file_version"])
nph5_file.close()
