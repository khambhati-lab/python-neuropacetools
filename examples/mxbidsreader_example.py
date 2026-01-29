""" mxbidsreader_example.py

"""
# Imports #
# Standard Libraries #
import os
import datetime
from pathlib import Path

# Third-Party Packages #
from blockobjects.process import DEFAULT_PROCESS_CONTEXT
from mxbids import Subject

# Local Packages #
from neuropacetools import neuropaceraw
from neuropacetools.neuropacecdfs import NEUROPACECDFS
from neuropacetools.neuropacecdfs.blocks import NEUROPACECDFSContentsUpdater
from neuropacetools.neuropacemxbids import NEUROPACEMXBIDSSession

# Definitions #
# Functions #
def main():

    # Setup #
    # PATHS
    raw_path = Path("/home/akhambhati/Holocron/scratch/NeuroPace_XX_51571 EXTERNAL #PHI")
    subject_identifier = "NeuroPace_XX_51571"
    mxbids_path = Path("./rns_subjects")

    # Create MXBIDS Subject
    mxbids_subject = Subject(
        name=subject_identifier,
        parent_path=mxbids_path,
        load=True,
        load_sessions=True,
        load_modalities=True)
    session_keys = [*mxbids_subject.sessions.keys()]
    session = mxbids_subject.sessions[session_keys[0]]
    cdfs = session.modalities["ieeg"].components["cdfs"].get_cdfs()
    print(cdfs.components["contents"].contents_table)
    print(dir(cdfs.components["contents"].contents_table))
    session =  cdfs.components["contents"].contents_table.create_session()
    print(session)

    """
    #proxy = cdfs.components["contents"].create_contents_proxy()
    proxy = cdfs.components["contents"].require_contents_proxy()

    T1 = proxy.start_datetime
    T2 = T1 + datetime.timedelta(days=7)
    stream_ecog = proxy.find_data_slice(T1, T2, approx=True, tails=True)
    print(stream_ecog)
    print(stream_ecog.axis[...]) 
    print(stream_ecog.data.shape)
    print(proxy.get_tzinfo())
    print(proxy.get_time_axis())
    """

# Main #
if __name__ == '__main__':
    main()

