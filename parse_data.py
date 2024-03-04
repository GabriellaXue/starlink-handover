from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

'''
Parse collected latency and throughput
'''
def parse_lt_tp() -> pd.DataFrame:
    lt_x = []
    lt_y = []
    tp_x = []
    tp_y = []

    with open("network_measurements.log", 'r') as file:
        for line in file:
            if "Lt" in line:
                results = line.strip().split(" Lt: ")
                dt_object = datetime.strptime(results[0], "%Y-%m-%d %H:%M:%S.%f")
                lt_x.append(dt_object)
                lt_y.append(float(results[1].split(" ")[0]))
            elif "TP" in line:
                results = line.strip().split(" TP: ")
                dt_object = datetime.strptime(results[0], "%Y-%m-%d %H:%M:%S.%f")
                tp_x.append(dt_object)
                tp_y.append(float(results[1].split(" ")[0]))

    # convert latency to data frame
    df_lt = pd.DataFrame({'timestamp': lt_x, 'latency': lt_y})
    df_lt.set_index('timestamp', inplace=True)
    df_resampled_lt = df_lt.resample('0.1s').mean() # handle overlap

    # convert throughput to data frame
    df_tp = pd.DataFrame({'timestamp': tp_x, 'throughput': tp_y})
    df_tp.set_index('timestamp', inplace=True)
    df_resampled_tp = df_tp.resample('0.1s').mean() # handle overlap

    # merge data frames with common timestamp
    merged_df = pd.merge(df_resampled_lt, df_resampled_tp, on='timestamp', how='inner')
    return merged_df

# plt.figure()
# plt.plot(df_resampled['timestamp'], df_resampled['value'])
# plt.xlabel("Epoch Time")
# plt.ylabel("Throughput(Mbps)")

# plt.show()

'''
Parse collected satellite data
'''
def parse_sat_measure() -> pd.DataFrame:
    sm_x = []
    sm_name = []
    sm_az = []
    sm_distance = []
    
    with open("sat_measurements.log", 'r') as file:
        for line in file:
            results = line.split(",")
            sm_x.append(datetime.fromtimestamp(round(float(results[0]))))
            sm_name.append(results[1].strip())
            sm_az.append(float(results[3].strip()))
            sm_distance.append(float(results[4].strip()))
    print(sm_x)
    df_sat = pd.DataFrame({'timestamp': sm_x, 'sat name': sm_name, 'az': sm_az, 'distance': sm_distance})

    df_sat.set_index(['timestamp', 'sat name'], inplace=True)
    df_resampled_sat = df_sat.groupby(level=[0, 1]).mean()
    df_resampled_sat.reset_index(inplace=True)

    # # Interpolate 1s data to 0.1 second
    # df_interpolation = df_resampled_sat.resample('0.1s').interpolate(method='linear') 

    return df_resampled_sat

'''
Match data sources
'''
def merge_data() -> pd.DataFrame:
    lt_tp = parse_lt_tp().resample('1s').mean()
    sat_measure = parse_sat_measure()
    return_df = pd.merge(lt_tp, sat_measure, on=['timestamp'], how='outer')
    return return_df

# Helper to locate what kind of duplicates do we have
def find_concurrent_sat():
    sat_measure = parse_sat_measure()
    grouped = sat_measure.groupby(level='timestamp')
    for idx, group in grouped:
        if len(group) > 1:
            print(group)

if __name__ == '__main__':
    merge_data().to_csv('data.csv', index=True)