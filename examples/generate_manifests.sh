#!/usr/bin/env bash
MXBIDS_DIR="/home/akhambhati/Holocron/remotes/hopfield/epilepsy_neuropace"
find "$MXBIDS_DIR" -type f -name "*.h5" > "$MXBIDS_DIR/MANIFEST_H5.txt"
