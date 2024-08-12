sudo sysctl -w net.ipv4.ip_forward=1
mm-link --meter-all --downlink-log='results/down.log' --uplink-log='results/up.log' uplink.log downlink.log python3 run_exp.py