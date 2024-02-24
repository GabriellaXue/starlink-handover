import subprocess
import re
import time
import csv
import threading
import queue
import signal
import sys

def signal_handler(sig, frame):
    exit_flag.set()
    print("Ctrl+C detected. Exiting...")
    ping_thread.join()
    iperf_thread.join()
    writer_thread.join()
    sys.exit(0)

def run_iperf(server_ip, iperf_queue):
    iperf_command = f"iperf3 -c {server_ip} -t 0 -i 0.1 -f m --forceflush"

    with subprocess.Popen(iperf_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        start_time = time.time()
        for output in process.stdout:
            line = output.strip()
            match = re.match(r'\[\s*\d+\]\s+\d+\.\d+-(\d+\.\d+)\s+sec\s+\d+\.?\d+?\s+[A-Za-z]+\s+(\d+\.?\d+?)\s+Mbits/sec', line)
            if match:
                interval, bitrate = match.groups()
                iperf_queue.put((start_time + float(interval), bitrate))
            if exit_flag.is_set():
                process.terminate()
                break
        process.wait()

def run_ping(server_ip, ping_queue):
    ping_command = f'ping {server_ip} -i 0.1'
    while not exit_flag.is_set():
        with subprocess.Popen(ping_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            for output in process.stdout:
                line = output.strip()
                match = re.search(r'time=(\d+\.?\d+?)\s+ms', line)
                if match:
                    rtt = match.groups()[0]
                    ping_queue.put((time.time(), rtt))
                if exit_flag.is_set():
                    process.terminate()
                    break
            process.wait()

def write_to_csv(ping_queue, iperf_queue):
    with open('output.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Timestamp', 'Bitrate(Mbps)', 'RTT(ms)'])

        while not exit_flag.is_set():
            if iperf_queue.empty() or ping_queue.empty():
                continue

            iperf_time, br = iperf_queue.get()
            ping_time, rtt = ping_queue.get()
            round_iperf_t = round(iperf_time, 1)
            round_ping_t = round(ping_time, 1)

            while round_iperf_t != round_ping_t:
                if round_iperf_t < round_ping_t:
                    iperf_time, br = iperf_queue.get()
                    round_iperf_t = round(iperf_time, 1)
                else:
                    ping_time, rtt = ping_queue.get()
                    round_ping_t = round(ping_time, 1)

            csv_writer.writerow([round(iperf_time, 1), br, rtt])
            csvfile.flush()

if __name__ == "__main__":
    server_ip = "172.202.73.177"
    
    iperf_queue = queue.Queue()
    ping_queue = queue.Queue()

    exit_flag = threading.Event()

    ping_thread = threading.Thread(target=run_ping, args=(server_ip, ping_queue))
    iperf_thread = threading.Thread(target=run_iperf, args=(server_ip, iperf_queue))
    writer_thread = threading.Thread(target=write_to_csv, args=(ping_queue, iperf_queue))

    signal.signal(signal.SIGINT, signal_handler)

    ping_thread.start()
    iperf_thread.start()
    writer_thread.start()

    ping_thread.join()
    iperf_thread.join()
    writer_thread.join()
