#!/usr/bin/env bash
MXBIDS_DIR="/home/akhambhati/Holocron/remotes/hopfield/epilepsy_neuropace"
FILELIST="$MXBIDS_DIR/MANIFEST_H5.txt"

# Define your function
clear_superblock() {
		file=$2
		h5clear -s $file
}

# Export the function
export -f clear_superblock

# Run the function in parallel
xargs -P 64 -n 1 -d '\n' bash -c 'clear_superblock "$@"' bash {} < "$FILELIST"
