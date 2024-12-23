from urllib.parse import urlparse
from environs import Env
import requests



def shorten_link(original_link, token, version):
    url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        "access_token": token,
        "v": version,
        "url": original_link,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    return response['response']['short_url']


def count_clicks(short_url, token, version):
    link_key = urlparse(short_url).path
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        "access_token": token,
        "v": version,
        "key": link_key[1:],
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    return response['response']['stats'][0]['views']


def is_shorten_link(original_link, token, version):
    url = 'https://api.vk.ru/method/utils.checkLink'
    params = {
        "access_token": token,
        "v": version,
        "url": original_link,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    return response['response']['link'] != original_link


def main():
    env = Env()
    env.read_env()

    access_token = env.str('ACCESS_TOKEN')
    version = env.float('VERSION')

    original_link = input("Введите ссылку")

    try:
        if is_shorten_link(original_link, access_token, version):
            print('кол-во кликов: ', count_clicks(original_link, access_token, version))
        else:
            print('сокращенная ссылка', shorten_link(original_link, access_token, version))
    except Exception as err:
        print('Ошибка, проверьте корректность ссылки')


if __name__ == '__main__':
    main()
