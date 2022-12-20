import os
from pprint import pprint
from datetime import datetime
from glob import glob
import pandas as pd

input_files_folder = os.path.abspath('input/')
input_files = glob(input_files_folder + '/*csv')

for file in input_files:
    if 'tasks' in file:
        tasks_df = pd.read_csv(file)
    elif 'answers' in file:
        answers_df = pd.read_csv(file)
    elif 'events' in file:
        events_df = pd.read_csv(file)
    else:
        print('No correct files in input folder!')

# Get first event date for user

events_for_first_count = ['start', 'get_task', 'answer']
first_event_dfs = []

for event in events_for_first_count:
    cond = events_df['event'] == event
    df = events_df.copy()[cond]
    first_event_df = df.groupby('tg_id').agg({'timestamp': 'min'})
    first_event_df[f'first_{event}_datetime'] = first_event_df['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x))
    first_event_df = first_event_df.drop(columns=['timestamp'])
    first_event_dfs.append(first_event_df)

first_events = pd.concat(first_event_dfs, axis=1)
pprint(first_events)

# Get last event date for user

events_for_last_count = ['answer']
last_event_dfs = {}

for event in events_for_last_count:
    print(event)
    cond = events_df['event'] == event
    df = events_df.copy()[cond]
    last_event_df = df.groupby('tg_id').agg({'timestamp': 'max'})
    last_event_df[f'last_{event}_datetime'] = last_event_df['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x))
    last_event_df = last_event_df.drop(columns=['timestamp'])
    last_event_dfs[event] = last_event_df
    pprint(last_event_df.head())


# To CSV

output_files_folder = os.path.abspath('output/')
filenames_dfs = {
    'user_first_events.csv': first_events,
    'user_last_events.csv': last_event_df
}

for filename, df in filenames_dfs.items():
    full_filename = output_files_folder + '/' + filename
    df.to_csv(full_filename)

