""" mxbidsexport_example.py.py

"""
# Imports #
# Standard Libraries #
import os
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
    # root_path = Path("/to/raw/neuropace/data/store")
    # subject_identifier = "RAW_SUBJECT_ID"
    mxbids_path = "./rns_subjects"

    ## Get Raw Data Objects
    ## Retrieve the catalog entry for a subject
    catalog = neuropaceraw.ieegcat('./Example_ECoG_Catalog.csv')

    for cat in catalog:
        ## Read the most recent catalog record entry
        ieeg_record = neuropaceraw.ieegget('./', cat)
        print(ieeg_record)
 
        # Create MXBIDS Subject
        mxbids_subject = Subject(
            name=cat.initials,
            parent_path=mxbids_path,
            mode="w",
            create=True
        )

        # Create MXBIDS Neuropace Session
        ses_name = f"neuropace-{cat.device_id}"
        if (session := mxbids_subject.sessions.get(ses_name, None)) is None:
            session = mxbids_subject.create_session(
               session=NEUROPACEMXBIDSSession,
               name=ses_name
            )
    
        # Create cdfs
        cdfs = session.modalities["ieeg"].components["cdfs"].require_cdfs()
        cdfs.name = mxbids_subject.name if cdfs.name is None else cdfs.name

        # create hdf5writer and contentupdater
        hdf5writer = cdfs.components["contents"].create_data_writer()
        contentsupdater = cdfs.components["contents"].create_contents_updater(
            will_proxy=False,
            init_setup=True
        )

        ## Convert the catalog entry to an hdf5 file
        filename = os.path.splitext(ieeg_record.catalog_entry.filename)[0]
        full_path, _ = cdfs.components["contents"].generate_file_path(filename)
        hdf5writer.evaluate(
            ieeg_record,
            full_path,
            file_remake=False,
            slice_=[None]
        )

        entry = cdfs.components["contents"].format_entry(filename) 
        contentsupdater.evaluate(entry=entry)


# Main #
if __name__ == '__main__':
    main()

