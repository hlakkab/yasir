from flask import Blueprint, render_template, request, flash, jsonify
import json
from .daily_data  import all_day_transformation, transform_data_to_df, get_best_tags_every_month
from .all_data  import monthly_data_transformation
from .read_data import read_the_csv_data_eploded, read_the_csv_data_exploded
from .best_questions import export_daily_data_with_specifique_tags, titles_Not_Similaire_with_Views, Top_titles_Not_Sim, get_best_q_every_month, read_data_from_csv
from .evolution import read_the_csv_data_evo,iterate_json_data ,have_json_one
from datetime import date
from flask_cors import CORS


views = Blueprint('views', __name__)
CORS(views)


@views.route('/', methods=['GET', 'POST'])
def home():
    #monthly_data_transformation()
    """    df = read_the_csv_data_eploded("01")
    #    df5 = all_day_transformation()
    json_data = df.to_json(orient='records')
    jsonify(json_data)
    """
    #get_best_q_every_month()
    helo = "helo"
    # Return the JSON data in the response body
    return helo

@views.route('/day', methods=['GET', 'POST'])
def day():

    #    df5 = all_day_transformation()
    df = read_the_csv_data_exploded()
    json_data = df.to_dict(orient='records')
    chart_data = [
        {
        "labels": [],
        "datasets": [
            {
                "label": "Tags Count",
                "data": [],
                "fill": False,
                "backgroundColor": "#2f4860",
                "borderColor": "#2f4860",
                "tension": 0.4
            }
        ]
    }
    ]
    for item in json_data:
        chart_data[0]["labels"].append(item["tags"])
        chart_data[0]["datasets"][0]["data"].append(item["count"])


    print(type(chart_data))
    print(chart_data)
    json_chart = json.dumps(json_data)

    # Return the JSON data in the response body
    return jsonify(json_data)

@views.route('/questions', methods=['GET', 'POST'])
def getquestions():
    df1 = read_best_question()
    df = titles_Not_Similaire_with_Views(df1)
    df2 = Top_titles_Not_Sim(df)

    json_data = df2.to_json(orient='records')
    # Return the JSON data in the response body
    return jsonify(json_data)

@views.route('/data')
def send_data():
    json_data = [
                 {'tags': 'spring-boot', 'count': 30},
                 {'tags': 'spring', 'count': 14},
                 {'tags': 'android', 'count': 11},
                 {'tags': 'spring-security', 'count': 8},
                 {'tags': 'hibernate', 'count': 6},
                 {'tags': 'gradle', 'count': 5},
                 {'tags': 'junit', 'count': 5},
                 {'tags': 'docker', 'count': 5},
                 {'tags': 'kotlin', 'count': 4}]

    return jsonify(json_data)
import pandas as pd

@views.route('/daa', methods=['GET'])
def get_data():
    df = pd.DataFrame({
        'tags': ['java', 'spring-boot', 'spring', 'android', 'spring-security', 'hibernate', 'gradle', 'junit', 'docker', 'kotlin'],
        'count': [89, 30, 14, 11, 8, 6, 5, 5, 5, 4]
    })

    json_data = df.to_dict(orient='records')

    return jsonify(json_data)

@views.route('/evo', methods=['GET'])
def evo_data():
    df_evo = read_the_csv_data_evo()
    have_json = have_json_one(df_evo)
    json_returned = iterate_json_data(have_json)
    formatted_json = json.loads(json_returned)

    return jsonify(formatted_json)

@views.route('/question_data', methods=['GET', 'POST'])
def filter_data():
    data = read_data_from_csv('C:/Users/LENOVO/pyver/stack_over_flow_data_analyses/month_q1.csv')

    selected_tags = request.json['tags']
    filtered_data = [row for row in data if any(tag in row['tags'] for tag in selected_tags)]
    return jsonify(filtered_data)
