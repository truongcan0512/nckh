#!/bin/bash
n=1     # number of switches
period=0

for i in {1..200000}
do
    # echo "Inspection no. $i at s$j"
    # extract essential data from raw data
    sudo ovs-ofctl dump-flows s2 > data/raw

    grep -E "nw_src|tcp" data/raw > data/flowentries.csv


    # Lay thong tin ve packet, byte, ipsrc, ipdst, psrc
    packets=$(awk -F "," '{split($4,a,"="); print a[2]","}' data/flowentries.csv)
    bytes=$(awk -F "," '{split($5,b,"="); print b[2]","}' data/flowentries.csv)
    ipsrc=$(awk -F "," '{split($15,c,"="); print c[2]","}' data/flowentries.csv)    #14 cho l3
    ipdst=$(awk -F "," '{split($16,d,"="); print d[2]","}' data/flowentries.csv)    #15 cho l3
    psrc=$(awk -F "," '{split($18,e,"="); print e[2]","}' data/flowentries.csv)     #17 cho l3
    idle_ages=$(awk -F "," '{split($8,e,"="); print e[2]","}' data/flowentries.csv)  
    # ipsrc=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($11,d,"="); print d[2]","}')
    # ipdst=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($12,d,"="); print d[2]","}')
    
    # check if there are no traffics in the network at the moment.
    if test -z "$packets" || test -z "$bytes" || test -z "$ipsrc" || test -z "$ipdst" || test -z "$idle_ages" 
    then
        state=0
    else

        period=$((period+1))
        
        if [ $period -eq 10 ]; then
            python3 computeTuples.py
            python3 inspector.py
            state=$(awk '{print $0;}' .result)

            > data/packets.csv
            > data/bytes.csv
            > data/ipsrc.csv
            > data/ipdst.csv
            > data/psrc.csv
            > data/idle_ages.csv
            period=0
        else
            echo "$packets" >> data/packets.csv
            echo "$bytes" >> data/bytes.csv
            echo "$ipsrc" >> data/ipsrc.csv
            echo "$ipdst" >> data/ipdst.csv
            echo "$psrc" >> data/psrc.csv
            echo "$idle_ages" >> data/idle_ages.csv
        fi
    fi

    if [ $state -eq 1 ];
    then
        echo 1 > /home/$USER/nckh/slow_result.txt
        #
        # default_flow=$(sudo ovs-ofctl dump-flows s$j | tail -n 1)    # Get flow "action:CONTROLLER:<port_num>" sending unknown packet to the controller
        # sudo ovs-ofctl del-flows s$j
        # sudo ovs-ofctl add-flow s$j "$default_flow"
    else
        echo 0 > /home/$USER/nckh/slow_result.txt
    fi

    sleep 1    # Because idle_timeout la 10s
done



# ==============================================================================================================================================
# Ref
# Get all fields (n columns) in awk: https://stackoverflow.com/a/2961711/11806074
# e.g. awk -F "," '{out=""; for(i=2;i<=NF;i++){out=out" "$i" "i}; print out}' data/flowentries.csv 

# ovs-ofctl reference
# add-flow SWITCH FLOW        add flow described by FLOW    e.g. ... add-flow s1 "flow info"
# add-flows SWITCH FILE       add flows from FILE           e.g. ... add-flows s1 flows.txt

# example of multiple commands in awk, these commands below extract ip_src and ip_dst from flow entries
# awk -F "," '{split($10,c,"="); print c[2]","}' data/flowentries.csv > data/ipsrc.csv
# awk -F "," '{split($11,d,"=");  split(d[2],e," "); print e[1]","}' data/flowentries.csv > data/ipdst.csv
