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
OUTPUT_PATH = "/home/akhambhati/Holocron/scratch/epilepsy_neuropace"

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
            catalog_path = [*source_path.glob(f"*Catalog*.csv")]
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


def _get_ieeg_record(
    catalog_entry,
    ROOT_PATH=ROOT_PATH
):
    file_path = [*ROOT_PATH.glob(f"*/*/*/{catalog_entry.filename}")]

    if len(file_path) > 1:
        print(f"Found {len(file_path)} DAT files for catalog entry.")
        file_sizes = [path.stat().st_size for path in file_path]
        file_path = file_path[file_sizes.index(max(file_sizes))]
    elif len(file_path) == 0:
        return None
    else:
        file_path = file_path[0]

    return neuropaceraw.ieegget(
        file_path.parent,
        catalog_entry
    )


def _get_mxbids_subject(
    npe_id,
    OUTPUT_PATH=OUTPUT_PATH
):
    return Subject(
        name=npe_id,
        parent_path=OUTPUT_PATH,
        mode="w",
        create=True
    )


def _get_mxbids_session(
    mxbids_subject,
    device_id
):

    ses_name = f"neuropace-{device_id}"
    if (session := mxbids_subject.sessions.get(ses_name, None)) is None:
        session = mxbids_subject.create_session(
           session=NEUROPACEMXBIDSSession,
           name=ses_name
        )
    return session


# Main #
if __name__ == '__main__':
    source = "current"

    registry = _get_registry()
    print(registry[9])

    pdms_id = registry[9]["pdms_id"]
    npe_id = registry[9]["npe_code"]
    date_of_birth = registry[9]["date_of_birth"]

    catalog = _get_catalog(
        source,
        pdms_id,
        date_of_birth
    )

    ieeg_record = _get_ieeg_record(
        catalog[0],
    )

    #######
    #######
    mxbids_subject = _get_mxbids_subject(
        npe_id,
        OUTPUT_PATH
    )

    mxbids_session = _get_mxbids_session(
        mxbids_subject,
        ieeg_record.catalog_entry.device_id
    )

    # Create cdfs object
    cdfs = mxbids_session.modalities["ieeg"].components["cdfs"].require_cdfs()
    cdfs.name = mxbids_subject.name if cdfs.name is None else cdfs.name

    # create hdf5writer and contentupdater
    hdf5writer = cdfs.components["contents"].create_data_writer()
    contentsupdater = cdfs.components["contents"].create_contents_updater(
        will_proxy=False,
        init_setup=True
    )
    #######
    #######

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
