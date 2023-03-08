#!/bin/bash

for i in {1..200000}
do
    end_host=$((RANDOM%16+2))
    python3 traffic.py -s 1 -e $end_host

    # socket=$((RANDOM%10+5))
    # python3 slowloris.py 10.0.0.1 -s $socket
    # sleep 4
    pgrep -a python3 | grep traffic.py | awk '{print $1}' | xargs kill

    # pgrep -a python | grep slowloris | pkill python


done