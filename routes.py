#!/usr/bin/env python
#*-* coding: utf-8 *-*

from flask import Flask
import flask

app = Flask(__name__)
app.debug = True

@app.route('/')
def weather_view():
  return flask.render_template('weather_view.html')

if __name__ == '__main__':
  app.run()
