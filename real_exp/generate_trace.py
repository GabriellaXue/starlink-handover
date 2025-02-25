import pandas as pd

def parse_log(file_name):
    df = pd.read_csv(file_name)
    return df

def write_trace(file_name, data, multiply):
    duration_ms = 1000
    timestamp = 1
    skip_flag = False

    with open(file_name, 'w') as file:
        for capacity in data:
            packet_number_per_ms = multiply * (capacity * 10 ** 6) / 1000 / 1504 / 8
            remainder = 0
            if packet_number_per_ms >= 1:
                for _ in range(duration_ms):
                    repeated_times = round(packet_number_per_ms)
                    remainder += packet_number_per_ms - repeated_times
                    if remainder >= 1:
                        repeated_times += 1
                        remainder -= 1
                    elif remainder <= -1:
                        repeated_times -= 1
                        remainder += 1
                    for _ in range(repeated_times):
                        file.write(str(timestamp) + '\n')
                    timestamp += 1
            else:
                for _ in range(duration_ms):
                    if round(packet_number_per_ms) == 0 and remainder < 1:
                        remainder += packet_number_per_ms
                        timestamp += 1
                        continue

                    if skip_flag:
                        skip_flag = False
                        continue
                    remainder -= round(packet_number_per_ms) - packet_number_per_ms
                    if remainder > 1 or remainder == 1:
                        timestamp += 1
                        remainder -= 1
                    elif remainder < -1 or remainder == -1:
                        skip_flag = True
                        remainder += 1
                    file.write(str(timestamp) + '\n')


def test(file, start, end):
    sum = 0
    with open(file, 'r') as lines:
        for line in lines:
            if int(line) >= start and int(line) <= end:
                sum += 1504
    print(sum * 8)


if __name__ == "__main__":
    df_measurements = parse_log("portal_measurements.csv")

    file_name = 'uplink.log'
    data = df_measurements['Uplink']
    write_trace(file_name, data, 0.1)

    file_name = 'downlink.log'
    data = df_measurements['Downlink']
    write_trace(file_name, data, 0.1)

    # test('downlink.log', 1, 1000)