#!/bin/bash
# arguments parsing
PARTS=$1
LINK_START_URLS=$2

# actual commands
for part in $(seq 0 $((PARTS-1))); do
    echo "Starting scrapyd job for part $part"
    curl http://localhost:6800/schedule.json -d project=wiki -d spider=wikipage -d link_start_url_list=$LINK_START_URLS -d parts_to_divide_into=$PARTS -d this_part_number=$part
done