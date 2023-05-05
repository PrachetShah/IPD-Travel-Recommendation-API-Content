import requests
from decouple import config

API_KEY = config('KEY')

def prompt(query):
    url = "https://api.writesonic.com/v2/business/content/ans-my-ques?num_copies=1"

    payload = {"question": query}

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": API_KEY
    }
    response = requests.post(url, json=payload, headers=headers)

    return response.text

# ans = prompt("generate a 2 day travel itinary plan for mumbai")
# print(ans)