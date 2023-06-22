import requests
import json

def get_news():
    BASE_URL = "https://saurav.tech/NewsAPI/"
    top_headlines_api = "https://saurav.tech/NewsAPI//top-headlines/category/business/in.json"
    # everything_api = "<BASE_URL>/everything/<source_id>.json"
    res = requests.get(top_headlines_api).json()
    response = res['articles'][0:6]
    return response

# print(res['articles'][0])
# 'title'
# 'description'
# url
# urlToImage
# publishedAt



