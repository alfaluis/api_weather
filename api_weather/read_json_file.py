import os
import json

root = os.getcwd()
database = os.path.join(root, 'city.list.json')


def load_city_list():
    with open(os.path.join(database, 'city_list.json'), 'r',encoding="utf8") as file:
        json_data = file.read()
        full_data = json.loads(json_data)
    return full_data


def get_matched_cities(full_data, param):
    cities_list = list()
    for data in full_data:
        if data['id'] == param:
            cities_list.append(data)
        elif data['name'] == param:
            cities_list.append(data)
        elif isinstance(param, list):
            if data['coord']['lat'] == param[0] and data[0]['coord']['lon'] == param[1]:
                cities_list.append(data)
    return cities_list

