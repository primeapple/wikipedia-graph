#!/bin/bash
# arguments parsing
PARTS=$1
if [ $# -eq 1 ]; then
    LINK_START_URLS='http://localhost:6800/items/wiki/articles/b091d6d0a32c11ea86f80242ac120002.jl'
else
    LINK_START_URLS=$2
fi

# actual commands
for part in $(seq 0 $((PARTS-1))); do
    echo "Starting scrapyd job for part $part"
    curl http://localhost:6800/schedule.json -d project=wiki -d spider=wikipage -d link_start_url_list=$LINK_START_URLS -d parts_to_divide_into=$PARTS -d this_part_number=$part
done