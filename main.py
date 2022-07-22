import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(token, parse_user_url):
    url = "https://api-ssl.bitly.com/v4/shorten"
    body = {
        "long_url": parse_user_url
    }
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()

    return response.json()["link"]


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


def is_bitlink(parse_user_url, token):
    header = {"Authorization" : "Bearer {}".format(token)}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{parse_user_url}"
    
    response = requests.get(url, headers=header)
    return response.ok

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    parse_user_url = argparse.ArgumentParser(
        description="Code that allows\
        you to shorten links using Bitly"
    )
    parse_user_url.add_argument('--url')
    
    args = parse_user_url.parse_args()
    
    parse_url= urlparse(args.url)
    
    if parse_url.scheme:
        parse_user_url = args.url
    else:
        parse_user_url = f"https://{args.url}"
    
    try:
        if is_bitlink(parse_user_url, token): 
            clicks_count = count_clicks(token, parse_user_url)
            print("Клики по ссылке = {}".format(clicks_count))
        else:
            bitlink = shorten_link(token, parse_user_url)
            print(bitlink)
    except requests.exceptions.HTTPError as error:
        print(error, "Что-то пошло не так...\nSomething went wrong...")
