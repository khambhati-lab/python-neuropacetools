""" mxbidsreader_ucsf.py

"""
# Imports #
# Standard Libraries #
import os
import datetime
from pathlib import Path
import sys

# Third-Party Packages #
from blockobjects.process import DEFAULT_PROCESS_CONTEXT
from mxbids import Subject

# Local Packages #
from neuropacetools import neuropaceraw
from neuropacetools.neuropacecdfs import NEUROPACECDFS
from neuropacetools.neuropacecdfs.blocks import NEUROPACECDFSContentsUpdater
from neuropacetools.neuropacemxbids import NEUROPACEMXBIDSSession

# Definitions #
module_path = os.path.abspath("/home/akhambhati/Holocron/repos/github.com/khambhati-lab/RNSFeatureExtractionPipeline/src/dataproc")
if module_path not in sys.path:
    sys.path.append(module_path)
import stimartifact

ROOT_PATH = Path("/home/akhambhati/Holocron/scratch/epilepsy_neuropace_badh5")
MXBIDS_PATH = Path("/home/akhambhati/Holocron/remotes/hopfield/epilepsy_neuropace")
ROOT_PATH.mkdir(exist_ok=True)

# Functions #
def main(inputs):

    # Setup #
    # PATHS
    subject_identifier = inputs["subject_identifier"]
    session_identifier = inputs["session_identifier"]


    # Create MXBIDS Subject
    mxbids_subject = Subject(
        name=subject_identifier,
        parent_path=MXBIDS_PATH,
        load=True,
        load_sessions=True,
        load_modalities=True)

    mxbids_session = mxbids_subject.sessions[session_identifier]
    cdfs = mxbids_session.modalities["ieeg"].components["cdfs"].get_cdfs()
    proxy = cdfs.components["contents"].require_contents_proxy()
    _ =  cdfs.components["contents"].contents_table.create_session()

    badh5_manifest_fn = ROOT_PATH / Path(f"sub-{mxbids_subject.name}_{session_identifier}_MANIFEST.csv")
    with open(badh5_manifest_fn, "w") as file:

        for ii, p in enumerate(proxy.flat_iterator()):
            try:
                print(ii)
                data = p.get_data()
                ts = p.get_nanostamps()
            except Exception as E:
                file.write(f"{p._path}\n")
                continue
    proxy.close()
    

# Main #
if __name__ == '__main__':
    subject_session_paths = [*MXBIDS_PATH.glob("sub-*/ses-*")]
    inputs = [{
        "subject_identifier": path.parts[-2].split("sub-")[-1],
        "session_identifier": path.parts[-1].split("ses-")[-1]
    } for path in subject_session_paths]


    from multiprocessing import Pool
    pool = Pool(32)
    pool.map(main, inputs)
