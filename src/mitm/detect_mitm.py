import math
import time
import random

class Mitm(object):
    def __init__(self) -> None:
        self.ip_mac = {}
        pass

    def start(self):
        # trich xuat ip_dst
        with open('/home/tiendat35/nckh/data/ipdst.csv', 'r') as ip1:
            file_ip_src = ip1.readlines()
        with open('/home/tiendat35/nckh/data/macdst.csv', 'r') as mac1:
            file_mac_src = mac1.readlines()
        i = 0
        while(i < len(file_ip_src)):
            self.ip_mac[file_ip_src[i]] = file_mac_src[i]
            i += 1

    def detect_mitm(self):
        flag = 0
        with open('/home/tiendat35/nckh/data/ipdst.csv', 'r') as ip1:
            file_ip_src = ip1.readlines()
        with open('/home/tiendat35/nckh/data/macdst.csv', 'r') as mac1:
            file_mac_src = mac1.readlines()
        i = 0
        #so sanh xem bo ip co gi khac khong
        while(i < len(file_ip_src)):
            if (self.ip_mac[file_ip_src[i]] != file_mac_src[i]):
                with open('/home/tiendat35/nckh/Mitm_result.txt', 'w') as f:
                    f.write("1")
                flag = 1
                break
                # print("detect attack!")
                i += 1
            else:
                with open('/home/tiendat35/nckh/Mitm_result.txt', 'w') as f:
                    f.write("0")
                # print("normal")
                flag = 0
                i += 1
        if (flag == 1):
            print("detect attack!")
        else:
            print("normal")
    

mitm_obj = Mitm()
mitm_obj.start()

while(1):
    start = time.time()
    mitm_obj.detect_mitm()
    end = time.time()
    x = 3 - (end - start)
    time.sleep(x)

