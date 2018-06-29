import os
import json


root = os.getcwd()
database = os.path.join(root, 'city.list.json')
with open(os.path.join(database, 'city_list.json'), 'r',encoding="utf8") as file:
    json_data = file.read()
    data = json.loads(json_data)

print(root)
json.loads(open(os.path.join(database, 'city_list.json')).read())