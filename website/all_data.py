import requests
from datetime import datetime
import json
from .daily_data  import transform_data_to_df, leave_data_related_to_java, export_daily_data
from dateutil.relativedelta import relativedelta
import os
import pandas as pd
import schedule
import time
import ast

def export_monthly_data():
    today = datetime.now().date()
    today_str = today.strftime('%Y-%m-%d')
    print(today_str)
    yesterday = today - relativedelta(months=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    print(yesterday_str)
    from_date = int(datetime.strptime(yesterday_str, '%Y-%m-%d').timestamp())
    to_date = int(datetime.strptime(today_str, '%Y-%m-%d').timestamp())
    # Set the page size and start with page 1
    pagesize = 100
    page = 1
    data_answers = []
    headers = {'Authorization': 'Bearer SsGHqKSiGKxxUUzehZbibw(('}
    site = 'stackoverflow'
    pagesize = 0
    data_test = []
    page = 1
    # Retrieve all pages of results
    while True:
        url = f'https://api.stackexchange.com/2.3/questions?site={site}&page={page}&fromdate={from_date}&todate={to_date}&key=SsGHqKSiGKxxUUzehZbibw(('
        response = requests.get(url)
        print(response)
        json_data = response.json()

        if 'items' in json_data:
                # Append the JSON data to the list
                data_answers.extend(json_data['items'])

                # Exit the loop if there are no more results
                if len(json_data['items']) == 0:
                    break
        else:
                # Handle the case when the 'items' key is not present in the JSON data
                print(f'ERROR: The JSON data does not contain the "items" key: {json_data}')
                break

        # Increment the page number to retrieve the next page of results
        page += 1
    return data_answers

def leave_data_by_10_tags(df,tag1 ,tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9, tag10):
    df1 = df[df['tags'].apply(lambda x: tag1 in x or tag2 in x or tag3 in x or tag4 in x or tag5 in x or tag6 in x or tag7 in x or tag8 in x or tag9 in x or tag10 in x )]
    return df1

def only_one_year(df, year):
    df = df[df['year'] == year]
    return df

def only_one_tag(df, tag):
    df = df[df['tags'] == tag]
    return df

def group_data_by_month(df):
    grouped = df.groupby(['tags', 'year', 'month']).size().reset_index(name='count')
    grouped_sorted = grouped.sort_values(['year', 'month', 'count'], ascending=False)
    return grouped_sorted

def extract_5_columns_from_df(df):
    tags_df = df[['tags','title','creation_date','view_count','answer_count']].copy()
    return tags_df

def add_monthly_data(df):
    today = datetime.now().date()
    # Create directory if it does not exist
    directory = f"C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/{today}.csv"
    if not os.path.exists(directory):
        df.to_csv(f"C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/{today}.csv", header=True, index=False)
        print("done")
    else:
        with open(f"C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/{today}.csv", 'a') as f:
            df.to_csv(f, header=False, index=False)
        print("exist")

import ast
def read_the_csv_data_eploded() :
    df_test = pd.read_csv('C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/all_final_data.csv')

    df_test['tags'] = df_test['tags'].apply(ast.literal_eval)
    df_test2 = df_test.explode('tags')

    return df_test2

def add_day_month_year(df):
    df['creation_date'] = pd.to_datetime(df['creation_date'], unit='s')

    # Create a new column for the month
    df['month'] = df['creation_date'].dt.month
    df['year'] = df['creation_date'].dt.year
    df['day'] = df['creation_date'].dt.day
    return df

def monthly_data_transformation():
    data = export_daily_data()
    df = transform_data_to_df(data)
    df1 = leave_data_related_to_java(df)
    df3 = extract_5_columns_from_df(df1)
    df4 = add_day_month_year(df3)
    add_monthly_data(df4)
    print("executed")
"""
schedule.every().month.at('01:01').do(monthly_data_transformation)

def every_month_data():
    while True:
        schedule.run_pending()
        time.sleep(1)
        if datetime.datetime.now().day == 1:
            # Clear the previously scheduled task
            schedule.clear('monthly_task')
            # Schedule the task again for the next month
            schedule.every().month.do(monthly_data_transformation)
"""