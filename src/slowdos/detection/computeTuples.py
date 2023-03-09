import numpy as np
import csv
import pandas as pd
from sklearn import preprocessing


time_interval = 1
window_size = 10

# ave_packets)
# slow-attack ave_packets low
packets_csv = np.genfromtxt('data/packets.csv', delimiter=",")
dt_packets = packets_csv[:,0]
ave_packets = np.average(dt_packets)
# appf = np.average(dt_packets)
# print(appf)


# ave_bytes
# slow-attack ave_bytes low
bytes_csv = np.genfromtxt('data/bytes.csv', delimiter=",")
dt_bytes = bytes_csv[:,0]
ave_bytes = np.average(dt_bytes)
# abpf = np.average(dt_bytes)
# print(abpf)
# print(ave_bytes)


# Number of flows per IP address (flows_per_ip)
# Attack flows_per_ip high
with open('data/ipsrc.csv', newline='') as f:
    reader = csv.reader(f)
    ipsrc_csv = list(reader)
f.close()
# dt_ipsrc = ipsrc_csv[:,0]
n_ip = len(np.unique(ipsrc_csv)) - 1      # Get number of different source IPs
num_flows = len(dt_packets) // window_size
flows_per_ip = num_flows // n_ip
# print(num_flows)


# std_idle_age
# attack std_idle_age high 
idle_ages_csv = np.genfromtxt('data/idle_ages.csv', delimiter=",")
dt_idle_ages = idle_ages_csv[:,0]
std_idle_age = np.std(dt_idle_ages)
# print(std_idle_age)

# Number of flows per interval time (new_flows_per_time_interval)
f = open('data/new_flows.txt', 'r')
new_flows_per_time_interval = int(f.read())
f.close()

headers = ["ave_packets", "ave_bytes", "flows_per_ip", "std_idle_age", "new_flows_per_time_interval"]

label = 0
features = [ave_packets, ave_bytes, flows_per_ip, std_idle_age, new_flows_per_time_interval]

standard_data = preprocessing.scale(features)
# data = standard_data.

# print(dict(zip(headers, features)))
# print("Standardize")
# print(standard_data)

# print(features)

# Uncomment when running 
with open('realtime.csv', 'w') as f:
    cursor = csv.writer(f, delimiter=",")
    # cursor.writerow(headers)
    cursor.writerow(standard_data)
    
    f.close()


# Create dataset-normal
# with open('data/dataset-normal.csv', 'a') as f:
#     cursor = csv.writer(f, delimiter=",")
#     # cursor.writerow(headers)
#     cursor.writerow(features)
    
#     f.close()


# Create dataset-attack
# with open('data/dataset-attack.csv', 'a') as f:
#     cursor = csv.writer(f, delimiter=",")
#     # cursor.writerow(headers)
#     cursor.writerow(features)
    
#     f.close()