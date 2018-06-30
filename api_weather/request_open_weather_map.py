import datetime
import json
import urllib.request
import requests


def url_builder(city_id, lat, lon, unit='metric', mode='json'):
    # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    user_api = 'ea5c35b4791d962238feca89f7ef2a52'  # Obtain yours form: http://openweathermap.org/

    api_weather = ['http://api.openweathermap.org/data/2.5/weather?id={0}&mode={1}&units={2}&APPID={3}',
                   'http://api.openweathermap.org/data/2.5/forecast?id={0}&mode={1}&units={2}&APPID={3}']
    api_uv = ['http://api.openweathermap.org/data/2.5/uvi?lat={0}&lon={1}&mode={2}&units={3}&APPID={4}',
              'http://api.openweathermap.org/data/2.5/uvi/forecast?lat={0}&lon={1}&mode={2}&units={3}&APPID={4}']
    full_api_list = list()
    for api in api_weather:
        full_api_list.append(api.format(city_id, mode, unit, user_api))
    for api in api_uv:
        full_api_list.append(api.format(lat, lon, mode, unit, user_api))
    return full_api_list


def data_fetch(full_api_url):
    keys = ['weather', 'forecast', 'uv', 'uv_forecast']
    idx = 0
    raw_api_dict = list()
    for url in full_api_url:
        response = requests.get(url, params=None)
        raw_api_dict.append(response.json())
        idx += 1
    return raw_api_dict

if __name__ == "__main__":
    full_url = url_builder(707860, 34.283333, 44.549999)
    print(data_fetch(full_api_url=full_url))
