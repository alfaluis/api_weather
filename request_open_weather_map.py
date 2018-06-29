import datetime
import json
import urllib.request


def url_builder(city_id, unit='metric', lat=None, lon=None):
    # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    user_api = 'ea5c35b4791d962238feca89f7ef2a52'  # Obtain yours form: http://openweathermap.org/
    api_weather = ['http://api.openweathermap.org/data/2.5/weather?id={0}',
                   'http://api.openweathermap.org/data/2.5/forecast?id={0}']
    api_uv = ['http://api.openweathermap.org/data/2.5/uvi?lat={0}&lon={1}',
              'http://api.openweathermap.org/data/2.5/uvi/forecast?lat={0}&lon={1}']
    full_api_list = list()
    for api in api_weather:
        full_api_list.append(api.format(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api)
    for api in api_uv:
        full_api_list.append(api.format(lat, lon) + '&mode=json&units=' + unit + '&APPID=' + user_api)
    return full_api_list


def data_fetch(full_api_url):
    keys = ['weather', 'forecast', 'uv', 'uv_forecast']
    idx = 0
    raw_api_dict = dict()
    for api in full_api_url:
        url = urllib.request.urlopen(full_api_url)
        output = url.read().decode('utf-8')
        raw_api_dict[keys[idx]] = json.loads(output)
        idx += 1
    url.close()
    return raw_api_dict

if __name__ == "__main__":
    full_url = url_builder(3873544)
    print(data_fetch(full_api_url=full_url))
