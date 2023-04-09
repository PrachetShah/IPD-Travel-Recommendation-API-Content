from faker import Faker
from faker.providers import DynamicProvider
import pandas as pd
import random

data = pd.read_csv('places.csv')
cities = list(set(data['City']))
print(len(cities))

generated_cities = []
generated_ages = []
generated_categories = []
generated_gender = []

# for city generation
city_names_provider = DynamicProvider(
     provider_name="city_generation",
     elements=cities,
)

# for category generation
categories_names_provider = DynamicProvider(
     provider_name="category_generation",
     elements=['Natural', 'Historical', 'Religious', 'Architectural'],
)

fake = Faker(['en_IN'])
# then add new provider to faker instance
fake.add_provider(city_names_provider)
fake.add_provider(categories_names_provider)

for _ in range(65):
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