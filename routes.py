#!/usr/bin/env python
#*-* coding: utf-8 *-*

from flask import Flask
import flask
import json

app = Flask(__name__)
app.debug = True

@app.route('/')
def weather_view():
  return flask.render_template('weather_view.html')

@app.route('weather.json')
def weather_json():
  # STATIC DATA
  # CHANGE THIS
  # JUST FOR TESTING
  return json.dumps({ 'temperature' : -5.5,
            'relative_humidity' : 85,
            'wind_speed' : 20,
            'wind_direction' : 0.75,
            'rainfall' : 2.4, 
            'barometer' : 101.3,
            'light' : 0.44 })

if __name__ == '__main__':
  app.run()
