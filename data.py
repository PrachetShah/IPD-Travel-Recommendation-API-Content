from faker import Faker
from faker.providers import DynamicProvider
from contentBased import *
import pandas as pd
import random

data = pd.read_csv('places.csv')
cities = list(set(data['City']))
places = list(set(data['Place']))
print(len(cities), len(places))

generated_cities = []
generated_ages = []
generated_categories = []
generated_gender = []
generated_Splace = []
generated_Dplace = []
generated_ratings = []

# for city generation
city_names_provider = DynamicProvider(
     provider_name="city_generation",
     elements=cities,
)

# for place generation
place_names_provider = DynamicProvider(
     provider_name="place_generation",
     elements=places,
)

# for category generation
categories_names_provider = DynamicProvider(
     provider_name="category_generation",
     elements=['Natural', 'Historical', 'Religious', 'Architectural'],
)

def data1():
     fake = Faker(['en_IN'])
     # then add new provider to faker instance
     fake.add_provider(city_names_provider)
     fake.add_provider(categories_names_provider)

     for _ in range(150):
          city = fake.city_generation()
          age = random.randint(10, 65)
          category = fake.category_generation()
          gender = random.choice(["Male", "Female"])

          generated_cities.append(city)
          generated_ages.append(age)
          generated_categories.append(category)
          generated_gender.append(gender)
          # print(city, age, category)

     # Calling DataFrame constructor on list
     data = {'City':generated_cities, 'Category':generated_categories, 'Age':generated_ages, 'Gender':generated_gender}
     df = pd.DataFrame(data)
     print(df.head())

     df.to_csv('profile_data.csv')

def data2():
     fake = Faker(['en_IN'])
     # then add new provider to faker instance
     fake.add_provider(city_names_provider)
     fake.add_provider(place_names_provider)
     fake.add_provider(categories_names_provider)

     df_places = pd.read_csv('places.csv')
     Splace = fake.place_generation()
     print(Splace)
     # places = Splace
     output = {}
     # Place id is [2251 'Mumbai' 'Marine Drive' 7500 1635 18] 
     id = df_places[df_places['Place']==Splace].values[0]
     # print(df_places[df_places['Place']==place]['PlaceID'])
     output[Splace] = recommend(id[3], num=1)
     print(output[Splace]['Suggested'][0][0])

     for _ in range(150):
          city = fake.city_generation()
          age = random.randint(10, 65)
          category = fake.category_generation()
          gender = random.choice(["Male", "Female"])
          rating = random.randint(1, 5)

          Splace = fake.place_generation()
          id = df_places[df_places['Place']==Splace].values[0]
          place2 = recommend(id[3], num=1)
          Dplace = place2['Suggested'][0][0]
          # print(Splace, Dplace)

          generated_cities.append(city)
          generated_Splace.append(Splace)
          generated_Dplace.append(Dplace)
          generated_ages.append(age)
          generated_categories.append(category)
          generated_gender.append(gender)
          generated_ratings.append(rating)
          # print(city, age, category)

     # Calling DataFrame constructor on list
     data = {'City':generated_cities, 'SPlace':generated_Splace, 'DPlace':generated_Dplace, 'Category':generated_categories, 'Age':generated_ages, 'Gender':generated_gender, 'Rating': generated_ratings}
     df = pd.DataFrame(data)
     print(df.head())

     df.to_csv('feedback_data.csv')

# data1()
data2()