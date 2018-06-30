import os
from flask import Flask, redirect, url_for, request, render_template
from api_weather.read_json_file import load_city_list, get_matched_cities
from api_weather.request_open_weather_map import url_builder, data_fetch
import json
import re
app = Flask(__name__)


def is_valid_mail(email):
    # Recordar que el método 'match()' retorna un objeto de tipo 'Match' que al ser
    # usado en sentencias como IF y WHILE representa un valor lógico. Podemos hacer
    # que una función retorne un valor lógico de la operación de match haciendo la
    # conversión a bool.
    #
    # Otra forma de escribir el patrón es:
    # pattern = "[a-zA-Z0-9_.]+@((seccion1|seccion2)\.)?(mi)?mail.cl"
    pattern = "[a-zA-Z0-9_.]+@((seccion1|seccion2)\.)?(gmail|mail).(cl|com)"
    return bool(re.match(pattern, email))

@app.route('/')
def index():
   return render_template('index.html')


@app.route('/success/<name>')
def success(name):
    return render_template('success.html')


@app.route('/getcity', methods=['POST'])
def get_weather():
    param = request.form['param']
    print(param)
    if len(param.split(',')) > 1:
        try:
            param = [float(x) for x in param.split(',')]
        except:
            raise ValueError
    else:
        try:
            param = int(param)
        except ValueError:
            pass
    cities = load_city_list()
    cities_asked = get_matched_cities(full_data=cities, param=param)
    print(type(cities_asked), len(cities_asked))
    for city in cities_asked:
        urls = url_builder(city_id=city['id'], lat=city['coord']['lat'], lon=city['coord']['lon'])
        info = data_fetch(full_api_url=urls)
        print(info[0])
        with open(os.path.join(os.getcwd(), city['name']) + '.txt', 'w') as file:
            file.write(str(info[1]['weather'][0]["description"]))
            file.write('\n')
            file.write(str(info[0]["main"]["temp"]))
            file.write('\n')
            file.write(str(info[0]["main"]["pressure"]))
            file.write('\n')
            file.write(str(info[0]["main"]["humidity"]))
            file.write('\n')
            file.write(str(info[0]["main"]["temp_min"]))
            file.write('\n')
            file.write(str(info[0]["main"]["temp_max"]))
            file.write('\n')
            file.write(str(info[0]["wind"]["speed"]))
            file.write('\n')
            file.write(str(info[0]["clouds"]["all"]))
    return json.dumps({"USUARIO": info[0], 'FORE': info[2]})


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form['email']
    if email == '':
        raise ValueError
    if not is_valid_mail(email):
        return render_template('index_error.html')
    else:
        return redirect(url_for('success', name=email))


if __name__ == '__main__':
    app.run(debug=True)