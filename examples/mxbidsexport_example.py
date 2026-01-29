""" mxbidsexport_example.py

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
    raw_path = Path("./raw_data")
    raw_path = Path("/home/akhambhati/Holocron/scratch/NeuroPace_XX_51571 EXTERNAL #PHI")
    subject_identifier = "ZZ"
    subject_identifier = "NeuroPace_XX_51571"
    mxbids_path = Path("./rns_subjects")

    ## Get Raw Data Objects
    ## Retrieve the catalog entry for a subject
    catalog = neuropaceraw.ieegcat(raw_path / Path(f"{subject_identifier}_ECoG_Catalog.csv"))

    # Create MXBIDS Subject
    mxbids_subject = Subject(
        name=subject_identifier,
        parent_path=mxbids_path,
        mode="w",
        create=True
    )

    # Create MXBIDS Neuropace Session
    ses_name = f"neuropace-{catalog[0].device_id}"
    if (session := mxbids_subject.sessions.get(ses_name, None)) is None:
        session = mxbids_subject.create_session(
           session=NEUROPACEMXBIDSSession,
           name=ses_name
        )

    # Create cdfs object
    cdfs = session.modalities["ieeg"].components["cdfs"].require_cdfs()
    cdfs.name = mxbids_subject.name if cdfs.name is None else cdfs.name

    # create hdf5writer and contentupdater
    hdf5writer = cdfs.components["contents"].create_data_writer()
    contentsupdater = cdfs.components["contents"].create_contents_updater(
        will_proxy=False,
        init_setup=True
    )

    # Iterate over iEEG records listed in the catalog
    for cat in catalog:
        print(cat)
        ## Read the most recent catalog record entry and retrieve iEEG record
        #ieeg_record = neuropaceraw.ieegget(raw_path, cat)
        ieeg_record = neuropaceraw.ieegget(
            Path("/home/akhambhati/Holocron/scratch/NeuroPace_XX_51571 EXTERNAL #PHI/NeuroPace_XX_51571 Data EXTERNAL #PHI"),
            cat
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
        hdf5writer.teardown()

        ## Upsert entry into the cdfs
        entry = cdfs.components["contents"].format_entry(filename) 
        contentsupdater.evaluate(entry=entry)

# Main #
if __name__ == '__main__':
    main()
