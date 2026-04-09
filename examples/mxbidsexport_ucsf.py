""" mxbidsexport_ucsf.py

"""
# Imports #
# Standard Libraries #
import csv
import os
from pathlib import Path

# Third-Party Packages #
#from blockobjects.process import DEFAULT_PROCESS_CONTEXT
from mxbids import Subject

# Local Packages #
from neuropacetools import neuropaceraw
from neuropacetools.neuropacecdfs import NEUROPACECDFS
from neuropacetools.neuropacecdfs.blocks import NEUROPACECDFSContentsUpdater
from neuropacetools.neuropacehdf5.fileobjects import NEUROPACEHDF5
from neuropacetools.neuropacemxbids import NEUROPACEMXBIDSSession


# Definitions #
ROOT_PATH = Path("/mnt/epilepsy_neuropace")
REGISTRY_PATH = ROOT_PATH / Path("registry") / Path("pdms_to_npe.csv")
OUTPUT_PATH = Path("/home/akhambhati/Holocron/remotes/hopfield/epilepsy_neuropace")
MANIFEST_H5_PATH = OUTPUT_PATH / Path("MANIFEST_H5.txt")
MANIFEST_DAT_PATH = REGISTRY_PATH / Path("MANIFEST_DAT.txt")


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

    master_catalog = []
    for cat_path in catalog_path:
        catalog = neuropaceraw.ieegcat(
            cat_path,
            new_reference_timestamp=date_of_birth
        )
        for cat in catalog:
            if cat.patient_id == int(pdms_id):
                master_catalog.append(cat)
    return master_catalog


def _get_ieeg_record(
    source,
    catalog_entry,
    ROOT_PATH=ROOT_PATH
):
    file_path = [*ROOT_PATH.glob(f"{source}/*/*/{catalog_entry.filename}")]

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


def _check_manifest(
    file_names, 
    MANIFEST_PATH=MANIFEST_H5_PATH
):
    in_manifest = [False] * len(file_names)
    with open(MANIFEST_PATH, "r") as f:
        for line in f:
            adjusted_line = line.split("\n")[0]
            if adjusted_line in file_names:
                in_manifest[file_names.index(adjusted_line)] = True
    return in_manifest


def _is_h5_clear(h5_path):
    try:
        loaded_file = NEUROPACEHDF5(file=h5_path, mode="r")
        loaded_file.close()
        return h5_path
    except:
        return None


def _regen_manifest(
    OUTPUT_PATH=OUTPUT_PATH,
    MANIFEST_PATH=MANIFEST_H5_PATH
):
    converted_h5 = [*OUTPUT_PATH.rglob("*.h5")]
    with open(MANIFEST_PATH, "w") as f:
        for ii, line in enumerate(converted_h5):
            print(ii)
            try:
                f.write(f"{line.resolve().as_posix().split('/')[-1].split('.')[0] + '.dat'}\n")
            except Exception as E:
                print(E)
                continue


def _append_manifest(
    file_name, 
    MANIFEST_PATH=MANIFEST_H5_PATH
):
    with open(MANIFEST_PATH, "a+") as f:
        f.write(f"{file_name}\n")


def main(inputs):
    registry_entry = inputs["registry_entry"]
    source = inputs["source"]
    
    pdms_id = registry_entry["pdms_id"]
    npe_id = registry_entry["npe_code"]
    date_of_birth = registry_entry["date_of_birth"]

    mxbids_subject = _get_mxbids_subject(
        npe_id,
        OUTPUT_PATH
    )

    catalog = _get_catalog(
        source,
        pdms_id,
        date_of_birth
    )

    in_manifest = _check_manifest([cat.filename for cat in catalog])
    for cat_i, cat in enumerate(catalog):
        if in_manifest[cat_i]:
            continue

        ieeg_record = _get_ieeg_record(source, cat)
        if ieeg_record is None:
            print(cat)
            print("ieeg_record is None")
            continue

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
       
        try:
            hdf5writer.evaluate(
                ieeg_record,
                full_path,
                file_remake=False,
                slice_=[None]
            )
        except Exception as E:
            print(E)
            os.remove(full_path)
            print(f"Removed: {full_path}")
            hdf5writer.evaluate(
                ieeg_record,
                full_path,
                file_remake=False,
                slice_=[None]
            )
            print(f"Rewrote: {full_path}")

        ## Upsert entry into the cdfs
        entry = cdfs.components["contents"].format_entry(filename) 
        contentsupdater.evaluate(entry=entry)

        _append_manifest(cat.filename)


# Main #
if __name__ == '__main__':
    import glob
    from multiprocessing import Pool
        
    registry = _get_registry()
    inputs = []
    for source in ["current", "v20190415"]:
        for registry_entry in registry:
            inputs.append(
                {"registry_entry": registry_entry,
                 "source": source})
    pool = Pool(32)
    pool.map(main, inputs)
