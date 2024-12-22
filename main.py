from urllib.parse import urlparse
from environs import Env
import requests
env = Env()
env.read_env()


def shorten_link(original_link):
    requests.get(original_link).raise_for_status()

    url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        "access_token": env.str("ACCESS_TOKEN"),
        "v": env.float("VERSION"),
        "url": original_link,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    return response['response']['short_url']


def count_clicks(short_url):
    requests.get(short_url).raise_for_status()

    link_key = urlparse(short_url).path
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        "access_token": env.str("ACCESS_TOKEN"),
        "v": env.float("VERSION"),
        "key": link_key[1:],
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    return response['response']['stats'][0]['views']


def is_shorten_link(original_link):
    requests.get(original_link).raise_for_status()

    url = 'https://api.vk.ru/method/utils.checkLink'
    params = {
        "access_token": env.str("ACCESS_TOKEN"),
        "v": env.float("VERSION"),
        "url": original_link,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    return response['response']['link'] != original_link


def main():
    original_link = input("Введите ссылку")

    try:
        if is_shorten_link(original_link):
            print('кол-во кликов: ', count_clicks(original_link))
        else:
            print('сокращенная ссылка', shorten_link(original_link))
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
