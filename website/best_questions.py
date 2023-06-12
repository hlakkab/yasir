import pandas as pd
import spacy
from .daily_data  import transform_data_to_df
from datetime import datetime, timedelta
import ast
import os
import csv
#Daily extracttion

import requests
from datetime import datetime, timedelta
def export_daily_data_with_specifique_tags(*tags):
    today = datetime.now().date()
    today_str = today.strftime('%Y-%m-%d')
    tags = list(tags)

    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    print(yesterday_str)
    # Set the site and date range for the analysis
    month = '2023-04-23'
    month1 = '2023-04-24'

    from_date = int(datetime.strptime(yesterday_str, '%Y-%m-%d').timestamp())
    to_date = int(datetime.strptime(today_str, '%Y-%m-%d').timestamp())

    site = 'stackoverflow'
    pagesize = 100
    data_test = []
    page = 1
    while True :
        url = f'https://api.stackexchange.com/2.3/questions?site={site}&pagesize={pagesize}&page={page}&fromdate={from_date}&todate={to_date}&key=SsGHqKSiGKxxUUzehZbibw(('
        tags = {
        'tagged': ';'.join(tags)
        }

        response = requests.get(url,params=tags)
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


def titles_Not_Similaire_with_Views(data_test):
    nlp = spacy.load('en_core_web_md')

    unique_titles = []
    view_counts_dict = {}
    answer_counts_dict = {}
    similar_titles_count = {}

    titles = data_test['title'].tolist()  # Convert the column to a list
    view_counts = data_test['view_count'].tolist()  # Convert the column to a list
    answer_counts = data_test['answer_count'].tolist()  # Convert the column to a list

    for i in range(len(titles)):
      title = titles[i]
      view_count = view_counts[i]
      answer_count = answer_counts[i]
      processed_title = nlp(title)

      if not any(processed_title.similarity(nlp(t)) > 0.5 for t in unique_titles):
          unique_titles.append(title)
          view_counts_dict[title] = view_count
          answer_counts_dict[title] = answer_count
          similar_titles_count[title] = 0
      else:
            for t in unique_titles:
                if processed_title.similarity(nlp(t)) > 0.5:
                    similar_titles_count[t] += 1

    df = pd.DataFrame({'title': unique_titles, 'view_count': [view_counts_dict[t] for t in unique_titles],
                       'answer_count': [answer_counts_dict[t] for t in unique_titles],
                       'similar_titles_count': [similar_titles_count[t] for t in unique_titles]})
    print(df)
    return df

def Top_titles_Not_Sim(df):
  df['view count'] = pd.to_numeric(df['view_count'])
  df['answer count'] = pd.to_numeric(df['answer_count'])

  df['similar titles count'] = pd.DataFrame(df['similar_titles_count'].astype(int))

  top_rows = df.nlargest(3, 'view count')
  top_df = pd.DataFrame({'Title': top_rows['title'], 'View Count': top_rows['view count'], 'Answer Count': top_rows['answer count'], 'Similar Titles Count': top_rows['similar titles count']})
  return(top_df)

def read_monthly_data():
    today = datetime.now().date()
    # Create directory if it does not exist
    df_best = pd.read_csv(f'C:/Users/LENOVO/Desktop/architecht/data_test.csv')
    return df_best



def read_data_from_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def add_monthly_data(df):
    today = datetime.now().date()
    # Create directory if it does not exist
    directory = f"C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/{today}_q.csv"
    if not os.path.exists(directory):
        df.to_csv(f"C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/{today}_q.csv", header=True, index=False)
        print("done")
    else:
        with open(f"C:/Users/LENOVO/Desktop/medium_proj_data/data/required_data/{today}_q.csv", 'a') as f:
            df.to_csv(f, header=False, index=False)
        print("exist")

def get_best_q_every_month():
    df = read_monthly_data()
    df1 = titles_Not_Similaire_with_Views(df)
    df2 = Top_titles_Not_Sim(df1)
    add_monthly_data(df2)


"""
schedule.every().month.at('02:01').do(get_best_q_every_month)

def every_month_questions():
    while True:
        schedule.run_pending()
        time.sleep(1)
        if datetime.datetime.now().day == 1:
            # Clear the previously scheduled task
            schedule.clear('monthly_task')
            # Schedule the task again for the next month
            schedule.every().month.do(get_best_q_every_month)"""