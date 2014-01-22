#!/usr/bin/env python
#*-* coding: utf-8 *-*

from flask import Flask
import flask
import config
import time, random

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

@app.route('/')
def weather_view():
  return flask.render_template('weather_view.html')

@app.route('/weather.json')
def weather_json():
  # STATIC DATA JUST FOR TESTING
  # This will eventually come from the daemon.
  weather_data = { 
            'temperature' : -5.5,                  # -5.5°C
            'relative_humidity' : 85,              # 85%
            'wind_speed' : int(random.random() * 100),  # 20 km/h
            'wind_direction' : random.random(),    # 270° (West)
            'rainfall' : 2.4,                      # 2.4 cm
            'barometer' : 101.3,                   # 101.3 kpa
            'light' : 0.44,                        # 44% intensity
            'time' : time.time() 
    }        
  return flask.jsonify(**weather_data)

if __name__ == '__main__':
  app.run(host='0.0.0.0')

