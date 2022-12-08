import pandas as pd
import numpy as np
import json
import random
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from tqdm import tqdm

df_places = pd.read_csv('num_ratings.csv')

# computing similarities requires too much resources on the whole dataset, so we take the subset with 100 items
df_places = df_places.reset_index(drop=True)

# we compute a TFIDF on the titles of the places
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(df_places['Place'])
# we get cosine similarities: this takes a lot of time on the real dataset
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
# we generate in 'results' the most similar cities for each place: we put a pair (score, place_id)
results = {}
for idx, row in df_places.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1] 
    similar_items = [(cosine_similarities[idx][i], df_places['PlaceID'].loc[[i]].tolist()[0]) for i in similar_indices] 
    results[idx] = similar_items[1:]

# transform a 'Place' into its corresponding City
def item(id):  
    return df_places.loc[df_places['PlaceID'] == id]['City'].tolist()[0].split(' - ')[0] 

# transform a 'place_id' into the index id
def get_idx(id):
    return df_places[df_places['PlaceID'] == id].index.tolist()[0]

# Finally we put everything together here:
def recommend(item_id, num):
    output = set()
    output.add(item(item_id))
    # print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")   
    # print("-------")    
    recs = results[get_idx(item_id)][:num]   
    for rec in recs: 
        output.add(item(rec[1]))
        # print("\tRecommended: " + item(rec[1]) + " (score:" +      str(rec[0]) + ")")
    output.remove(item(item_id))
    return output


# for _ in range(5):
#     recommend(random.choice(df_places[df_places['City']=='Mumbai']['PlaceID'].unique()), num=10)