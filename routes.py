#!/usr/bin/env python
#*-* coding: utf-8 *-*

from flask import Flask
import flask
import json
import httplib
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
  conn = httplib.HTTPConnection(config.Config.DATA_SOURCE)
  conn.request("GET", "/index.html")
  ajax_resp = conn.getresponse()
  if ajax_resp.status == 200:
    provider_data = json.loads(ajax_resp.read())
    
    weather_data = { 
      'temperature' : provider_data['serial']['temperature'],
      'relative_humidity' : provider_data['serial']['relative_humidity'],
      'wind_speed' : provider_data['serial']['wind_speed'],
      'wind_direction' : provider_data['serial']['wind_direction'],
      'rainfall' : provider_data['serial']['rain_sensor'],
      'barometer' : provider_data['serial']['barometer'] / 1000, #kPa
      'light' : provider_data['serial']['light'],
      'time' : time.time() 
    }
    
  return flask.jsonify(weather_data)
  #return flask.jsonify(**weather_data)
  return redirect("http://localhost:8000");

if __name__ == '__main__':
  app.run(host='0.0.0.0')

