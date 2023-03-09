#!/bin/bash


for i in {1..200000}
do
    sudo ovs-ofctl dump-flows s2 > isEmpty.txt
    if [ `cat isEmpty.txt | wc -l` -eq 1 ]; then
        stateEntropy=0
        stateSVM=0
        stateMitm=0
        stateSlow=0
        echo "Normal state"
    else
        stateEntropy=$(awk '{print $0;}' /home/$USER/nckh/src/resultEntropy.txt)
        stateSVM=$(awk '{print $0;}' /home/$USER/nckh/src/resultSVM.txt)
        stateMitm=$(awk '{print $0;}' /home/$USER/nckh/src/resultMitM.txt)
        stateSlow=$(awk '{print $0;}' /home/$USER/nckh/src/resultSlow.txt)
        

        if [ $stateEntropy -eq 1 ];
        then
            if [ $stateSVM -eq 0 ];
            then
                echo "Warning: Abnormal detection"
                #echo 0 >> check.txt
            # elif [ $stateSVM -eq 1 & $stateMitm -eq 1]
            #     echo "Both Attack"
            else
                echo "Happening DDoS attack"
            fi
        else
            if [ $stateMitm -eq 1 ];
            then    
                echo "Happening MitM attack"
            elif [ $stateSlow -eq 1 ];
            then
                echo "Happening Slow attack"
            else
                echo "Normal state"
            fi
        fi
    fi
    
sleep 2
done
