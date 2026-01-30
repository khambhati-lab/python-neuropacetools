""" mxbidsexport_ucsf.py

"""
# Imports #
# Standard Libraries #
import csv
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
ROOT_PATH = Path("/mnt/epilepsy_neuropace")
REGISTRY_PATH = ROOT_PATH / Path("registry") / Path("pdms_to_npe.csv")

# Functions #
def _get_registry(REGISTRY_PATH=REGISTRY_PATH):
    with open(REGISTRY_PATH, "r") as file:
        reader = csv.DictReader(file, delimiter=",")
        rows = [*reader]
    return rows


def _get_catalog(
    source,
    pdms_id, 
    date_of_birth,
    ROOT_PATH=ROOT_PATH
): 

    source_path = ROOT_PATH / Path(source)
    match source:
       case "current":
            catalog_path = [*source_path.glob(f"*_{pdms_id} */*Catalog*.csv")]
       case "v20190415":
            catalog_path = [*source_path.glob(f"*Catalog.csv*")]
    if len(catalog_path) != 1:
        print(f"Found {len(catalog_path)} catalog files.")
        return None
    catalog_path = catalog_path[0]
    catalog = neuropaceraw.ieegcat(
        catalog_path,
        new_reference_timestamp=date_of_birth
    )
    catalog = [cat for cat in catalog if cat.patient_id == int(pdms_id)]
    return catalog

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
    registry = _get_registry()

    print(_get_catalog("current", registry[0]["pdms_id"], registry[0]["date_of_birth"]))
