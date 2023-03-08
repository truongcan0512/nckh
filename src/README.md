#NCKH2023
This project is about detect DDoS, MitM, and Slow DoS attack in SDN
TO RUN this program, followwing this steps:

1. Run topology and controller

Copy file l2_edited and detectionUsingEntropy.py to /home/pox/forwarding

sudo mn --topo=tree,depth=2,fanout=4 --switch=ovsk --controller=remote,ip=127.0.0.1,port=6633

sudo pox.py forwarding.l2_edited


2. Run program detect Slow DoS

source /home/nckh/src/slowdos/detection collect.sh
source /home/nckh/src/slowdos/detection new_flows.sh

3. Run program detect all attack types

source /home/truong/nckh23/src/collect-flows.sh
source /home/truong/nckh23/src/run.sh

4. Open host 1 and run it as a server

python3 /home/nckh/src/slowdos/server/server.py 10.0.0.1 -p 80 -s 150

5. Attack

#Attack DDoS
hping3 --rand-source --flood 10.0.0.1

#Attack Slow DoS

python3 /home/nckh/src/slowloris/traffic/attack.sh

#Attack MitM



