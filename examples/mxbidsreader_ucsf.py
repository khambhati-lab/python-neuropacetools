""" mxbidsreader_ucsf.py

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
    subject_identifier = "NPE0010"
    mxbids_path = Path("/home/akhambhati/Holocron/remotes/hopfield/epilepsy_neuropace")

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
    session =  cdfs.components["contents"].contents_table.create_session()

    #proxy = cdfs.components["contents"].create_contents_proxy()
    proxy = cdfs.components["contents"].require_contents_proxy()
    print(dir(proxy))

    for ii, p in enumerate(proxy.flat_iterator()):
        print(ii)
        print(p.get_data()[...].shape)
        print(p.get_nanostamps()[...].shape)
        p.close()
    """
    T1 = proxy.start_datetime
    T2 = T1 + datetime.timedelta(days=7)
    stream_ecog = proxy.find_data_slice(T1, T2, approx=True, tails=True)
    print(stream_ecog)
    """

# Main #
if __name__ == '__main__':
    main()

