import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(token, long_url):
    url = "https://api-ssl.bitly.com/v4/shorten"
    body = {
        "long_url": long_url
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
    header = {
        "Authorization": "Bearer {}".format(token)
    }

    response = requests.get(url.format(
        netloc=parsed_bitlink.netloc,
        path=parsed_bitlink.path),
        headers=header)
    response.raise_for_status()

    return response.json()["total_clicks"]


def is_bitlink(url, token):
    header = {"Authorization": "Bearer {}".format(token)}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}"

    response = requests.get(url, headers=header)
    return response.ok


if __name__ == "__main__":
    load_dotenv()
    bitly_token = os.getenv("BITLY_TOKEN")
    parser = argparse.ArgumentParser(
        description="Code that allows\
        you to shorten links using Bitly"
    )
    parser.add_argument('--url')

    args = parser.parse_args()

    parse_url = urlparse(args.url)
    user_url = args.url

    try:
        if is_bitlink(user_url, bitly_token):
            clicks_count = count_clicks(bitly_token, user_url)
            print("Клики по ссылке = {}".format(clicks_count))
        else:
            bitlink = shorten_link(bitly_token, user_url)
            print(bitlink)
    except requests.exceptions.HTTPError as error:
        print(error, "Что-то пошло не так...\nSomething went wrong...")
