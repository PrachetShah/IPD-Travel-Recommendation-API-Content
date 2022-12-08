import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from tqdm import tqdm

recommender = pd.read_csv('places.csv')
# print(recommender.head())
df = recommender.reset_index(drop=True)

# we compute a TFIDF on the titles of the places
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(df['Place'])
# we get cosine similarities: this takes a lot of time on the real dataset
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
# we generate in 'results' the most similar cities for each place: we put a pair (score, place_id)
results = {}
for idx, row in df.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1] 
    similar_items = [(cosine_similarities[idx][i], df['PlaceID'].loc[[i]].tolist()[0]) for i in similar_indices] 
    results[idx] = similar_items[1:]

# transform a 'Place' into its corresponding City
def item(id):  
    return df.loc[df['PlaceID'] == id]['Place'].tolist()[0].split(' - ')[0] 

# transform a 'place_id' into the index id
def get_idx(id):
    return df[df['PlaceID'] == id].index.tolist()[0]
# Finally we put everything together here:
def recommend(item_id, num):
    output = {}
    # print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")   
    # print("-------")    
    output["Suggested"] = []
    recs = results[get_idx(item_id)][:num]   
    for rec in recs: 
        place = item(rec[1])
        output["Suggested"].append([item(rec[1]), df.loc[df["Place"]==item(rec[1])]["ImageUrl"].tolist()])
        # output["Image"].append(df.loc[df["Place"]==item(rec[1])]["ImageUrl"].tolist())
        # print("\tRecommended: " + item(rec[1]) + " (score:" +      str(rec[0]) + ")")
    return output