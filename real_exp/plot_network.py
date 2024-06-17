'''
We following the below rules to interprete mahimahi logs:
1. e.g. 958 + 80; 958 + 52
    This refers to timestamp 958 ms has 132 bytes received by packet queue.
2. e.g. 968 - 80 10; 968 - 52 10
    This refers to timestamp 968 ms has one packet with 80 bytes delivered that delays by 10ms and 
    the other packet with 52 bytes delivered that delays by 10ms. We take the summation for packet
    sizes and we take the max for queuing delay as both packets are processed concurrently.
3. e.g. 968 # 1504
    This refers to timestamp 968ms has a delivery opportunity of 1504 bytes.
4. TODO: packet drop
'''
import pandas as pd
import matplotlib.pyplot as plt


def parse_logs(file_name):
    bandwidths = []
    throughputs = []

    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue

            values = line.split()
            timestamp = int(values[0])
            packet_size = int(values[2])

            if '#' in values:
                timestamp, _, bytes_value = line.split()
                bandwidths.append((int(timestamp), int(bytes_value)))
            elif '-' in values:
                timestamp, _, bytes_value, delay = line.split()
                throughputs.append((int(timestamp), int(bytes_value), int(delay)))
    
    return bandwidths, throughputs


def create_dataframes(bandwidths, throughputs):
    bandwidth_frame = pd.DataFrame(bandwidths, columns=['timestamp', 'bytes'])
    throughput_frame = pd.DataFrame(throughputs, columns=['timestamp', 'bytes', 'delay'])

    return bandwidth_frame, throughput_frame

def aggregate_data(bandwidth_frame, throughput_frame):
    # For bandwidth, aggregate ms to s level
    bandwidth_frame['timestamp'] = (bandwidth_frame['timestamp'] // 1000) * 1000
    bandwidth_frame_agg = bandwidth_frame.groupby('timestamp').sum()

    # For throughput, aggregate ms to s level for bytes and use max delay for each ms
    throughput_frame['timestamp_sec'] = (throughput_frame['timestamp'] // 1000) * 1000
    throughput_frame_bytes_agg = throughput_frame.groupby('timestamp_sec')['bytes'].sum()
    throughput_frame_delay_agg = throughput_frame.groupby('timestamp')['delay'].max()

    return bandwidth_frame_agg, throughput_frame_bytes_agg, throughput_frame_delay_agg


def convert_bps_to_mbps(df_bandwidth, df_throughput):
    df_bandwidth['bytes'] = df_bandwidth['bytes'] / (10 ** 6)
    df_throughput = df_throughput / (10 ** 6)
    return df_bandwidth, df_throughput


def plot_data(bandwidth_bytes, throughput_bytes, throughput_delays):
    fig, ax1 = plt.subplots(figsize=(12, 8))

    color = 'tab:blue'
    ax1.set_xlabel('Timestamp (ms)')
    ax1.set_ylabel('Bandwidth/Throughput (MB)', color=color)
    ax1.fill_between(bandwidth_bytes.index, bandwidth_bytes['bytes'], color='#40798C', alpha=0.4, label='Bandwidth')
    plt.plot(throughput_bytes.index, throughput_bytes, color='#1F363D', label='Throughput')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('Delay (ms)', color=color)
    ax2.fill_between(throughput_delays.index, throughput_delays, color='orange', alpha=0.4, label='Delay (ms)')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('Network Performance Simulation')
    fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
    plt.show()

if __name__ == "__main__":
    bandwidths, throughputs = parse_logs("results/down.log")
    bandwidth_frame, throughput_frame = create_dataframes(bandwidths,throughputs)
    b_b, t_b, t_d = aggregate_data(bandwidth_frame, throughput_frame)
    b_mb, t_mb = convert_bps_to_mbps(b_b, t_b)
    plot_data(b_mb, t_mb, t_d)






        
            
