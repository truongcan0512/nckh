#!/bin/bash
for i in {1..200000}
do
    count1=$(sudo ovs-ofctl dump-flows s2 | wc -l)
    sleep 9
    count2=$(sudo ovs-ofctl dump-flows s2 | wc -l)
    flow_entry_count=$((count2-count1))

    echo $(( $flow_entry_count > 0 ? $flow_entry_count : -$flow_entry_count )) > data/new_flows.txt

done