import os
from pprint import pprint
from datetime import datetime
from glob import glob
import pandas as pd

# READ INPUT CSVs TO DFs

input_files_folder = os.path.abspath('input/')
input_files = glob(input_files_folder + '/*csv')

for file in input_files:
    if 'tasks' in file:
        tasks_df = pd.read_csv(file)
    elif 'answers' in file:
        answers_df = pd.read_csv(file)
    elif 'events' in file:
        print("No processing Events")
    else:
        print('No correct files in input folder!')

# TO DATETIME

tasks_df['task_date'] = pd.to_datetime(tasks_df['task_date'], format="%d.%m.%Y")
tasks_df['task_date'] = tasks_df['task_date'].dt.date

answers_df['answer_date'] = pd.to_datetime(answers_df['answer_date'], format="%d.%m.%Y")
answers_df['answer_date'] = answers_df['answer_date'].dt.date

answers_df['answer_datetime'] = pd.to_datetime(answers_df['answer_datetime'], format="%d.%m.%Y %H:%M:%S")

# GET USER

# Left only unique answers from user on date
answers_unique = answers_df.copy().sort_values('answer_datetime')
answers_unique = answers_unique.drop_duplicates(subset=['tg_id', 'answer_date'])

pprint(len(answers_df))
pprint(len(answers_unique))

