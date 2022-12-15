import pandas as pd
import os
from pprint import pprint
from datetime import datetime


def get_interval(series):
    diff_series = series.diff()

    # Only intervals less than N seconds

    interval_threshold = 30
    diff_series_cond = diff_series < interval_threshold
    diff_series = diff_series[diff_series_cond]
    interval = round(diff_series.median(), 1)

    return interval


# Read Events CSV
events_path = os.path.abspath('input/events_raw_2022-12-14_18-11.csv')
events = pd.read_csv(events_path, index_col='transaction_id')

# Get datetime, date and transform timestamp from str to float
events['datetime'] = events['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x))
events['date'] = events['datetime'].dt.date
events['timestamp'] = pd.to_numeric(events['timestamp'])

events.sort_values('datetime').to_clipboard()

# Events to count interval between

events_interval_dict = {
    'start_interval': ['start', 'start_reply'],
    'task_interval': ['get_task', 'get_task_reply'],
    'answer_interval': ['answer', 'answer_reply'],
    'stats_interval': ['stats', 'stats_reply']
}

# List to collect dfs with all intervals to concat
all_intervals = []

for new_col_name, events_for_calc in events_interval_dict.items():
    # Filter df - left only events for calc

    events_cond = events['event'].isin(events_for_calc)
    calc_events = events.copy()[events_cond].sort_values('datetime')

    # Calculate interval
    interval_df = calc_events.groupby(['date', 'name']).agg({'timestamp': get_interval})
    interval_df = interval_df.rename(columns={'timestamp': new_col_name})

    all_intervals.append(interval_df)

result_df = pd.concat(all_intervals, axis=1)
pprint(result_df)
pprint(result_df.info())


result_df.to_csv('intervals.csv')

# value = 1671006846.806126
# pprint(str(int(round(value, 0))))
# pprint(str(int(value)))


