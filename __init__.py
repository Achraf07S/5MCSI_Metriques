from flask import Flask, render_template, jsonify
from urllib.request import urlopen
from datetime import datetime
from collections import Counter
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def contact():
    return render_template('contact.html')

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

            results.append({
                'Jour': dt_object.strftime('%Y-%m-%d %H:%M:%S'),
                'temp': round(temp_celsius, 2)
            })

    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/commits/data/')
def commits_data():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))

    minutes_list = []
    for commit in data:
        commit_date = commit.get('commit', {}).get('author', {}).get('date')
        if commit_date:
            date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
            minutes_list.append(date_object.minute)

    counter = Counter(minutes_list)
    return jsonify(counter)

@app.route('/commits/')
def commits_page():
    return render_template('commits.html')

if __name__ == "__main__":
    app.run(debug=True)
