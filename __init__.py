from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
#commit                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_kelvin = list_element.get('main', {}).get('temp')
        
        if dt_value is not None and temp_kelvin is not None:
            temp_celsius = temp_kelvin - 273.15
            dt_object = datetime.utcfromtimestamp(dt_value)

            if dt_object.date() == today:
                results.append({
                    'Jour': dt_object.strftime('%Y-%m-%d %H:%M:%S'),
                    'temp': round(temp_celsius, 2)
            })

    return jsonify(results=results)
  
if __name__ == "__main__":
  app.run(debug=True)
