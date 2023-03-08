#!/bin/bash

stateEntropy=0
stateSVM=0

for i in {1..2000000}
do
    stateEntropy=$(awk '{print $0;}' /home/tiendat35/nckh/resultEntropy.txt)
    stateSVM=$(awk '{print $0;}' /home/tiendat35/nckh/hybrid-model/resultSVM.txt)

    if [ $stateEntropy -eq 1 ]
    then
        if [ $stateSVM -eq 0 ]
        then
            echo "Warning: Abnormal detection"
            echo 0 >> check.txt
        else
            echo "Network is under attack"
            echo 1 >> check.txt
        fi
    else
        echo "Network is normal"
        echo 0 >> check.txt
    fi
sleep 2
done

