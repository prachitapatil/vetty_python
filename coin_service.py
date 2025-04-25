import requests


def get_all_coins():
    res = requests.get("https://api.coingecko.com/api/v3/coins/list")
    return res.json() if isinstance(res.json(), list) else []

def get_categories():
    res = requests.get("https://api.coingecko.com/api/v3/coins/categories/list")
    return res.json()

def get_filtered_coins(ids=None):
    params = {
        "vs_currency": "cad",
        "ids": ids
    }
    res = requests.get("https://api.coingecko.com/api/v3/coins/markets", params=params)
    return res.json()
