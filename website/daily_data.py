import requests
from datetime import datetime, timedelta
import pandas as pd
import schedule
import time
import os
import ast
def export_daily_data():
    today = datetime.now().date()
    today_str = today.strftime('%Y-%m-%d')

    yesterday = today - timedelta(days=3)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    print(yesterday_str)
    # Set the site and date range for the analysis


    from_date = int(datetime.strptime(yesterday_str, '%Y-%m-%d').timestamp())
    to_date = int(datetime.strptime(today_str, '%Y-%m-%d').timestamp())

    site = 'stackoverflow'
    pagesize = 0
    data_test = []
    page = 1
    while True :
        url = f'https://api.stackexchange.com/2.3/questions?site={site}&page={page}&fromdate={from_date}&todate={to_date}&key=SsGHqKSiGKxxUUzehZbibw(('

        response = requests.get(url)
        print(response)
        json_data = response.json()

        if 'items' in json_data:
                    # Append the JSON data to the list
                    data_test.extend(json_data['items'])

                    # Exit the loop if there are no more results
                    if len(json_data['items']) == 0:
                        break
        else:
                    # Handle the case when the 'items' key is not present in the JSON data
                    print(f'ERROR: The JSON data does not contain the "items" key: {json_data}')
                    break

            # Increment the page number to retrieve the next page of results
        page += 1
    return data_test

def transform_data_to_df(list):
    df = pd.DataFrame(list)
    return df

def leave_data_related_to_java(df):
    df1 = df[df['tags'].apply(lambda x: 'java' in x or 'spring' in x or 'spring-mvc' in x or 'spring-boot' in x or 'spring-data' in x or 'spring-security' in x or 'hibernate' in x or 'jpa' in x or 'rest' in x or 'servlets' in x or 'jsp' in x or 'thymeleaf' in x or 'maven' in x or 'gradle' in x or 'junit' in x or 'mockito' in x or 'log4j' in x or 'slf4j' in x)]
    return df1

def extract_2_columns_from_df(df):
    tags_df = df[['tags', 'creation_date']].copy()
    return tags_df

def explode_readed_tags(df):
    df['tags'] = df['tags'].apply(ast.literal_eval)
    tags_df = df.explode('tags')
    return tags_df

def explode_tags(df):
    tags_df = df.explode('tags')
    return tags_df

def best_10_tags_per_day(df):
    tag_counts = df['tags'].value_counts().sort_values(ascending=False).reset_index()
    tag_counts.columns = ['tags', 'count']
    # Get the top 10 tags
    top_tags = tag_counts.head(20)
    return top_tags

def all_day_transformation():
    data = export_daily_data()
    df = transform_data_to_df(data)
    df1 = leave_data_related_to_java(df)
    df3 = extract_2_columns_from_df(df1)
    df4 = explode_tags(df3)
    df5 = best_10_tags_per_day(df4)
    return df5

def read_monthly_data():
    today = datetime.now().date()
    # Create directory if it does not exist
    df_best = pd.read_csv(f'C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/{today}.csv')
    return df_best

def add_daily_data(df):
    today = datetime.now().date()
    # Create directory if it does not exist
    directory = f"C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/{today}_t.csv"
    if not os.path.exists(directory):
        df.to_csv(f"C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/{today}_t.csv", header=True, index=False)
        print("done")
    else:
        with open(f"C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/{today}_t.csv", 'a') as f:
            df.to_csv(f, header=False, index=False)
        print("exist")

def get_best_tags_every_month():
    df = read_monthly_data()
    df1 = extract_2_columns_from_df(df)
    df2 = explode_readed_tags(df1)
    df3 = best_10_tags_per_day(df2)
    add_daily_data(df3)



# Schedule function 1 to run every 2 minutes
"""
schedule.every().month.at('02:01').do(get_best_tags_every_month)

def every_month_tags():
    while True:
        schedule.run_pending()
        time.sleep(1)
        if datetime.datetime.now().day == 1:
            # Clear the previously scheduled task
            schedule.clear('monthly_task')
            # Schedule the task again for the next month
            schedule.every().month.do(get_best_tags_every_month)

"""