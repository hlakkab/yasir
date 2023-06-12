import pandas as pd
import json

def read_the_csv_data_evo() :
    df_test = pd.read_csv('C:/Users/LENOVO/Desktop/architecht/tags_evolution/evo.csv')

    return df_test

def have_json_one(df_leave):
    json_data = df_leave.to_dict(orient='records')
    return json_data

def iterate_json_data(json_data):
    transformed_data = {}

    for item in json_data:
        tag = item['tags']
        month = item['month'].lower()
        count = item['count']

        # Check if the tag already exists in the transformed data dictionary
        if tag in transformed_data:
            transformed_data[tag]['callCount'][month] = count
        else:
            transformed_data[tag] = {
                'tag': tag,
                'callCount': {month: count}
            }

    values_list = [value for value in transformed_data.values()]

    # Convert the result to JSON string
    json_str = json.dumps(values_list, indent=4)

    return json_str