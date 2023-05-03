from flask import Flask, request
import pandas as pd
import numpy as np
from contentBased import *
import random 
from itinerary import prompt

app = Flask(__name__)

# Places Recommender
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
                id = df_places[df_places['Place']==place].values[0]
                # print(df_places[df_places['Place']==place]['PlaceID'])
                output[place] = recommend(id[3], num=10)
        return output

# Itinerary Generator
@app.route('/chat', methods=['POST'])
def chatbot():
    if request.method=='POST':
        data = request.json
        # print(data['msg'])
        res = prompt(data['msg'])
        # print(res)
        return res
    return {'output': 'invalid method'}

# City Recommendations
@app.route('/city', methods=['POST'])
def find_places():
    if request.method == 'POST':
        data = request.json

        city = data['city']
        output = {}

        # cities = pd.read_csv('Updated.csv')
        num_ratings = pd.read_csv('num_ratings.csv')
        df_places = pd.read_csv('places.csv')

        for CITY in city:
            try:
                my_dict = dict()
                places = list(num_ratings[num_ratings['City']==CITY]['Place'])

                for x,y in zip(places, list(num_ratings[num_ratings['City']==CITY]['Num_of_Rating'])):
                    my_dict[x] = y

                sorted_keys = sorted(my_dict, key=lambda x: my_dict[x], reverse=True)

                # Convert the sorted keys into a dictionary
                sorted_dict = dict([(key, my_dict[key]) for key in sorted_keys[:7]])
                images = {}
                for place, val in sorted_dict.items():
                    images[place] = df_places[df_places['Place']==place].values[0][-1]
                # output[CITY] = {'output':True, 'num':len(places), 'places':sorted_dict, 'images':images}
                output[CITY] = {'output':True, 'num':len(places), 'images':images}
            except Exception as e:
                output[CITY] = {'output':False}
        return output

# City Recommendation based on Tourist Data
@app.route('/topCity')
def feedback():
    df_places = pd.read_csv('feedback_data.csv')
    cities = list(set(df_places['City']))
    output = {}
    for city in cities:
        num = len(df_places[df_places['City']==city]['Rating'])
        rating = sum(df_places[df_places['City']==city]['Rating'])
        avgRating = round(rating/num, 2)
        # print(city, num, rating, avgRating)
        # Recommending Formula
        score = round(num*0.3 + avgRating, 2)
        output[city] = {'Num Visited': num, 'avgRating': avgRating, 'score': score}
    # Sorting Dict based on score
    output = sorted(output.items(), key=lambda x: x[1]['score'], reverse=True)

    return {'response':output}

# Places Recommendation based on age
@app.route('/byAge', methods=['POST'])
def byAge():
    if request.method == 'POST':
        agegrp = request.json
        grp = agegrp['age']
        print(grp)
        output = {}
        df_places = pd.read_csv('places.csv')
        if grp == 'y':
            place = 'Solang Valley'
            id = df_places[df_places['Place']==place].values[0]
            # print(df_places[df_places['Place']==place]['PlaceID'])
            output[grp] = recommend(id[3], num=7)
        elif grp == 'k':
            place = 'Nariman Point'
            id = df_places[df_places['Place']==place].values[0]
            # print(df_places[df_places['Place']==place]['PlaceID'])
            output[grp] = recommend(id[3], num=7)
        elif grp == 'a':
            place = 'Ramoji Film City'
            id = df_places[df_places['Place']==place].values[0]
            # print(df_places[df_places['Place']==place]['PlaceID'])
            output[grp] = recommend(id[3], num=7)
        elif grp=='s':
            place = 'Jagdish Temple'
            id = df_places[df_places['Place']==place].values[0]
            # print(df_places[df_places['Place']==place]['PlaceID'])
            output[grp] = recommend(id[3], num=7)
        return output

    return {'response':'Wrong Method'}

if __name__ == '__main__':
    app.run(debug=True)