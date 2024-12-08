import requests


def requests_get(url, params=None, headers=None):
    return requests.get(url=url, headers=headers, params=params)


def requests_post(url, json=None, headers=None):
    return requests.post(url=url, headers=headers, json=json)
