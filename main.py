from flask import Flask, request
import pandas as pd
import numpy as np
from contentBased import *
import random 

app = Flask(__name__)

@app.route('/placeName', methods=['POST'])
def hello():
    if request.method == 'POST':
        data = request.json

        df_places = pd.read_csv('places.csv')
        places = data['place']
        output = {}
        for place in places:
            if place in df_places['Place'].unique():
                # Place id is [2251 'Mumbai' 'Marine Drive' 7500 1635 18] 
                print(df_places[df_places['Place']==place].values)
                id = df_places[df_places['Place']==place].values[0]
                print(df_places[df_places['Place']==place]['PlaceID'])
                output[place] = recommend(id[3], num=10)
        return output

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


if __name__ == '__main__':
    app.run(debug=True)