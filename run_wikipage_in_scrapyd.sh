#!/bin/bash
# arguments parsing
PARTS=$1
COLLECTION=$2
LINK_START_URLS=$3


# actual commands
for part in $(seq 0 $((PARTS-1))); do
    echo "Starting scrapyd job for part $part"
    scrapyd-client schedule -p wiki --arg link_start_url_list=$LINK_START_URLS --arg parts_to_divide_into=$PARTS --arg this_part_number=$part --arg collection=$COLLECTION wikipage
done