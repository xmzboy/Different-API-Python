import requests
import grequests
import json


def connection(places, place):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={places[place][0]}&lon={places[place][1]}&appid=8537d9ef6386cb97156fd47d832f479c'
    return url


def one_connect(lats, lons):
    params = {'lat': lats, 'lon': lons, 'appid': '8537d9ef6386cb97156fd47d832f479c'}
    url = 'https://api.openweathermap.org/data/2.5/weather'
    with requests.Session() as sess:
        try:
            r = sess.get(url, params=params, timeout=1)
        except Exception as ex:
            print(ex)
            return {}
        else:
            return r.json()


def get_responses_lst(places):
    places_urls = []
    for place in range(len(places)):
        places_urls.append(connection(places, place))

    async_list = []
    for u in places_urls:
        action_item = grequests.get(u)
        async_list.append(action_item)

    lst = []

    for resp in grequests.map(async_list):
        lst.append(json.loads(resp.text))

    return lst
