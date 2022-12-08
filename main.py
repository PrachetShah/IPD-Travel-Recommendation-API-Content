from flask import Flask, request
import pandas as pd
import numpy as np
# from cityRecommendation import *
import random 

app = Flask(__name__)

@app.route('/')
def hello():
    # df_places = pd.read_csv('num_ratings.csv')
    # output = recommend(random.choice(df_places[df_places['City']=='Mumbai']['PlaceID'].unique()), num=10)
    return f'Hello'

@app.route('/city', methods=['POST'])
def find_places():
    if request.method == 'POST':
        data = request.json

        city = data['city']
        output = {}

        # cities = pd.read_csv('Updated.csv')
        num_ratings = pd.read_csv('num_ratings.csv')

        for CITY in city:
            try:
                my_dict = dict()
                places = list(num_ratings[num_ratings['City']==CITY]['Place'])

                for x,y in zip(places, list(num_ratings[num_ratings['City']==CITY]['Num_of_Rating'])):
                    my_dict[x] = y

                sorted_keys = sorted(my_dict, key=lambda x: my_dict[x], reverse=True)

                # Convert the sorted keys into a dictionary
                sorted_dict = dict([(key, my_dict[key]) for key in sorted_keys[:10]])
                output[CITY] = {'output':True, 'num':len(places), 'places':sorted_dict}
            except Exception as e:
                output[CITY] = {'output':False}
        return output

# @app.route('/recommendCity', methods=['POST'])
# def recommend():


if __name__ == '__main__':
    app.run(debug=True)