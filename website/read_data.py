import ast
import pandas as pd
import requests
from datetime import datetime, timedelta
import pandas as pd
import schedule
import time
import os
import ast




def group_data_by_month(df):
    grouped = df.groupby(['tags', 'year', 'month']).size().reset_index(name='count')
    grouped_sorted = grouped.sort_values(['year', 'month', 'count'], ascending=False)
    return grouped_sorted

def read_the_csv_data_eploded(month) :
    df_test = pd.read_csv(f'C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/2023-{month}-01.csv')

    df_test['tags'] = df_test['tags'].apply(ast.literal_eval)
    df_test2 = df_test.explode('tags')

    df_grouped = group_data_by_month(df_test2)
    df_grouped = df_grouped.head(1)

    return df_grouped

def read_the_csv_data_exploded() :
    today = datetime.now().month
    if today < 10:
        today =f'0{today}'

    df_test = pd.read_csv(f'C:/Users/LENOVO/pyver/stack_over_flow_data_analyses/2023-{today}-01.csv')

    """    df_test['tags'] = df_test['tags'].apply(ast.literal_eval)
    df_test2 = df_test.explode('tags')

    df_grouped = group_data_by_month(df_test2)
    df_grouped = df_grouped.head(10)"""

    return df_test

