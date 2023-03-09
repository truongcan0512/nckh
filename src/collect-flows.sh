#!/bin/bash
for i in {1..5000000}
do
    start=`date +%s.%N`
    # extract essential data from raw data
    sudo ovs-ofctl dump-flows s2 > data/raw.txt
    grep "nw_src" data/raw.txt > data/flowentries.csv
    ipsrc=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($14,d,"="); print d[2]","}')
    ipdst=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($15,d,"="); print d[2]","}')
    macsrc=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($12,d,"="); print d[2]","}')
    macdst=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($13,d,"="); print d[2]","}')
    
    
    # check if there are no traffics in the network at the moment.
    if test -z "$ipsrc" || test -z "$ipdst" || test -z "$macdst" || test -z "$macsrc" 
    then
        state=0
    else
        echo "$ipsrc" > data/ipsrc.csv
        echo "$ipdst" > data/ipdst.csv
        echo "$macsrc" > data/macsrc.csv
        echo "$macdst" > data/macdst.csv
        
    fi
    echo "collect compeletly"
    end=`date +%s.%N`
    runtime=$( echo "$end - $start" | bc -l )
    timesleep=$( echo "3 - $runtime" | bc -l )
    sleep $timesleep
done


