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

ROOT_PATH = Path("/home/akhambhati/Holocron/scratch/epilepsy_neuropace_artifacts")
MXBIDS_PATH = Path("/home/akhambhati/Holocron/remotes/hopfield/epilepsy_neuropace")

# Functions #
def main(inputs):

    # Setup #
    # PATHS
    subject_identifier = inputs["subject_identifier"]

    # Create MXBIDS Subject
    mxbids_subject = Subject(
        name=subject_identifier,
        parent_path=MXBIDS_PATH,
        load=True,
        load_sessions=True,
        load_modalities=True)

    for session_key in mxbids_subject.sessions.keys():
        mxbids_session = mxbids_subject.sessions[session_key]
        cdfs = mxbids_session.modalities["ieeg"].components["cdfs"].get_cdfs()
        proxy = cdfs.components["contents"].require_contents_proxy()
        _ =  cdfs.components["contents"].contents_table.create_session()

        artifacts_manifest_fn = ROOT_PATH / Path(f"sub-{mxbids_subject.name}_{session_key}_MANIFEST.csv")
        with open(artifacts_manifest_fn, "a+") as file:

            for ii, p in enumerate(proxy.flat_iterator()):
                data = p.get_data()
                ts = p.get_nanostamps()
                artifacts = stimartifact.detect_stim_artifacts(
                    signalmat=data,
                    params={
                        "NUMCHAN": data.shape[1],
                        "MIN_ARTIFACT_LENGTH": 10,
                        "POST_STIM_BUFFER": 100
                    }
                )[0]
                p.close()
                
                for artifact in artifacts:
                    file.write(f"{ts[artifact[0]]},{ts[artifact[1]-1]}\n")

# Main #
if __name__ == '__main__':
    inputs = [{"subject_identifier": "NPE0010"}]
    main(inputs[-1])

