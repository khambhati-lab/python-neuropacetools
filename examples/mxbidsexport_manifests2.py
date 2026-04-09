""" mxbidsexport_ucsf.py

"""
# Imports #
# Standard Libraries #
from pathlib import Path

# Third-Party Packages #
import numpy as np

# Local Packages #

# Definitions #
ROOT_PATH = Path("/mnt/epilepsy_neuropace")
REGISTRY_PATH = ROOT_PATH / Path("registry") / Path("pdms_to_npe.csv")
OUTPUT_PATH = Path("/home/akhambhati/Holocron/remotes/hopfield/epilepsy_neuropace")
MANIFEST_PATH = OUTPUT_PATH / Path("MANIFEST.txt")
if not MANIFEST_PATH.exists():
    f = open(MANIFEST_PATH, "w+")
    f.close()


from pathlib import Path

def compare_files_by_filename(file_a_path, file_b_path):
    """
    Compares the filenames between two files containing lists of paths.

    Args:
        file_a_path (str): The path to the first text file.
        file_b_path (str): The path to the second text file.

    Returns:
        list: A list of full file paths from File A whose filenames 
              do not appear in File B.
    """
    
    # 1. Read the paths from the input files
    paths_a = file_a_path.read_text().strip().splitlines()
    paths_b = file_b_path.read_text().strip().splitlines()
    
    # 2. Extract filenames and create a set for efficient lookups
    # The .name attribute from pathlib is used to get the filename.
    filenames_a = {Path(p).stem for p in paths_a}
    filenames_b = {Path(p).stem for p in paths_b}
    
    # 3. Find file paths in list A whose filenames are not in the set of filenames from list B
    unique_paths_a = [
        path_a for path_a in paths_a 
        if Path(path_a).stem not in filenames_b
    ]

    return unique_paths_a


# Main #
if __name__ == '__main__':

    MANIFEST_DAT = OUTPUT_PATH / Path("MANIFEST_DAT.txt")
    MANIFEST_H5 = OUTPUT_PATH / Path("MANIFEST_H5.txt") 

    paths_not_in_b = compare_files_by_filename(MANIFEST_DAT, MANIFEST_H5)
    paths_not_in_b_subjects = {path.split('/')[4] for path in paths_not_in_b}
    for subject in paths_not_in_b_subjects:
        count = 0
        for path in paths_not_in_b:
            if subject in path:
                count += 1
        print(subject, count)


    #print("File paths in list_a.txt with filenames not present in list_b.txt:")
    #for path in paths_not_in_b:
    #    print(path.split('/'))

