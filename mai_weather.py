import os
from flask import Flask, redirect, url_for, request, render_template
from api_weather.read_json_file import load_city_list, get_matched_cities
from api_weather.request_open_weather_map import url_builder, data_fetch
import json
app = Flask(__name__)


@app.route('/')
def index():
   return render_template('index.html')


@app.route('/success/<name>')
def success(name):
    return render_template('sucess.html')


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
        with open(os.path.join(os.getcwd(), city['name']) + '.txt', 'w') as file:
            file.write(str(info[0]['weather']))
    return json.dumps({"USUARIO": info[0], 'FORE': info[2]})


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        param = request.form['param']
        email = request.form['email']
        if email == '':
            raise ValueError
        return redirect(url_for('success', name=email))
    else:
        user = request.args.get('id')
        country = request.form['country']
        return redirect(url_for('success', name=user))

if __name__ == '__main__':
    app.run(debug=True)