import json
import matplotlib.pyplot as plt
import sys

candidate_id = sys.argv[1]

file_path = 'webrtc_internals_dump_receive.json'

with open(file_path, 'r') as file:
    data = json.load(file)

datetime_list = []
bytes_received = []
bytes_sent = []
rtt = []
lost = []
total = []
received = []

for conn_key, conn_val in data['PeerConnections'].items():
    for stat_key, stat_val in conn_val['stats'].items():
        if candidate_id + "-timestamp" in stat_key and stat_val['statsType'] == "candidate-pair":
            string_vals = stat_val['values'][1:-1].split(',')
            datetime_list += [float(val) for val in string_vals]
        if candidate_id + "-[bytesReceived_in_bits/s]" in stat_key and stat_val['statsType'] == "candidate-pair":
            string_vals = stat_val['values'][1:-1].split(',')
            bytes_received += [float(val) for val in string_vals]
        if candidate_id + "-[bytesSent_in_bits/s]" in stat_key and stat_val['statsType'] == "candidate-pair":
            string_vals = stat_val['values'][1:-1].split(',')
            bytes_sent += [float(val) for val in string_vals]
        if candidate_id + "-currentRoundTripTime" in stat_key and stat_val['statsType'] == "candidate-pair":
            string_vals = stat_val['values'][1:-1].split(',')
            rtt += [float(val) for val in string_vals]
        if candidate_id + "-packetsDiscardedOnSend" in stat_key and stat_val['statsType'] == "candidate-pair":
            string_vals = stat_val['values'][1:-1].split(',')
            lost += [float(val) for val in string_vals]
        if candidate_id + "-packetsSent" in stat_key and stat_val['statsType'] == "candidate-pair":
            string_vals = stat_val['values'][1:-1].split(',')
            total += [float(val) for val in string_vals]
        if candidate_id + "-packetsReceived" in stat_key and stat_val['statsType'] == "candidate-pair":
            string_vals = stat_val['values'][1:-1].split(',')
            received += [float(val) for val in string_vals]


plt.plot(datetime_list, bytes_received, label='Downlink Capacity (bits/s)')
plt.plot(datetime_list, bytes_sent, label='Uplink Capacity (bits/s)')
plt.plot(datetime_list, rtt, label='rtt (s)')
plt.plot(datetime_list, [lost[i] / total[i] for i in range(len(lost))], label='pkt lost rate')
plt.plot(datetime_list, total, label='total pkt sent')
plt.plot(datetime_list, received, label='total pkt received')
plt.title('WebRTC Analysis')
plt.xlabel('datetime')
plt.ylabel('value')
plt.legend()
plt.show()