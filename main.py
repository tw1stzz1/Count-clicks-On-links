import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, long_url):
    url = "https://api-ssl.bitly.com/v4/shorten"
    body = {"long_url": long_url}
    header = {"Authorization": "Bearer {}".format(token)}

    response = requests.post(url, json=body, headers=header)
    response.raise_for_status()

    return response.json()["id"]


def count_clicks(token, bitlink):
    parsed_bitlink = urlparse(bitlink)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{netloc}{path}/clicks/summary"
    header = {"Authorization": "Bearer {}".format(token)}

    response = requests.get(url.format(
        netloc=parsed_bitlink.netloc,
        path=parsed_bitlink.path),
        headers=header)
    response.raise_for_status()

    return response.json()["total_clicks"]


def is_bitlink(url, token):
    header = {"Authorization" : "Bearer {}".format(token)}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}"
    
    response = requests.get(url, headers=header)
    return response.ok

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    url = argparse.ArgumentParser()
    url.add_argument('name', nargs='?')

    try:
        if is_bitlink(url, token): 
            clicks_count = count_clicks(token, url)
            print("Клики по ссылке = {}".format(clicks_count))
        else:
            bitlink = shorten_link(token, url)
            print(bitlink)
    except requests.exceptions.HTTPError:
        print("Что-то пошло не так...\nSomething went wrong...")
