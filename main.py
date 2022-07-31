import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(bitly_token, parser):
    url = "https://api-ssl.bitly.com/v4/shorten"
    body = {
        "long_url": parser
    }
    headers = {
        "Authorization": "Bearer {}".format(bitly_token)
    }
    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()

    return response.json()["link"]


def count_clicks(bitly_token, bitlink):
    parsed_bitlink = urlparse(bitlink)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{netloc}{path}/clicks/summary"
    header = {
        "Authorization": "Bearer {}".format(bitly_token)
    }

    response = requests.get(url.format(
        netloc=parsed_bitlink.netloc,
        path=parsed_bitlink.path),
        headers=header)
    response.raise_for_status()

    return response.json()["total_clicks"]


def is_bitlink(parser, bitly_token):
    header = {"Authorization": "Bearer {}".format(bitly_token)}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{parser}"

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
    parser = args.url

    try:
        if is_bitlink(parser, bitly_token):
            clicks_count = count_clicks(bitly_token, parser)
            print("Клики по ссылке = {}".format(clicks_count))
        else:
            bitlink = shorten_link(bitly_token, parser)
            print(bitlink)
    except requests.exceptions.HTTPError as error:
        print(error, "Что-то пошло не так...\nSomething went wrong...")
