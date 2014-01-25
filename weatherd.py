#!/usr/bin/env python
#*-* coding: utf8 *-*

import os, sys
import json
import tornado.ioloop
import tornado.web
import serial

import math

PRECISION = 1 # Round to one decimal place for derivative calculations
DEVICE = '/dev/ttyACM0'
PORT = 8000

# Human-readable translations:
FROSTBITE_DANGER = BetweenDict(
  { (-35, -26) : 'Danger of frostbite in 30 minutes',
    (-35, -45) : 'Danger of frostbite in 10 minutes',
    (-45, -sys.maxint) : 'Danger of frostbite in 5 minutes or less' })

DEWPOINT = BetweenDict(
  { (26, sys.maxint) : 'Severely high.  Fatal to Asthma-related illnesses',
    (24, 26) : 'Extremely uncomfortable',
    (21, 24) : 'Very uncomfortable',
    (18, 21) : 'Somewhat uncomfortable',
    (16, 18) : 'Mostly comfortable',
    (13, 16) : 'Comfortable',
    (10, 12) : 'Very comfortable',
    (-sys.maxint, 10) : 'Dry' })
    
HEATSTROKE = BetweenDict(
  { (27, 32) : 'Caution: Fatigue possible with prolonged activity',
    (32, 41) : 'Extreme caution: Heat exhaustion or stroke possible.',
    (41, 54) : 'Danger: Heat exhaustion likely. Danger of heat stroke',
    (54, sys.maxint) : 'Extreme danger: Heat stroke is imminent' })
  

serialPending = ''

#called whenever there is new input to check
mostRecentLine = ''

def checkSerial():
  global serialPending
  try:
    serial_data = ser.read(ser.inWaiting())
  except :
    print("Error reading from %s " % serialPort )
    return
    
  if len(serial_data) > 0:
    serialPending += serial_data
    parseSerial()
    
def parseSerial():
  global mostRecentLine
  global serialPending
  packets = serialPending.split("\n")
  if len(packets) > 1:
    for line in packets[0:-1]:
      print(line)
      mostRecentLine = line      

  pending = packets[-1]
  serialPending = ''
  
# handle commands sent from the web browser
class CommandHandler(tornado.web.RequestHandler):
  #both GET and POST requests have the same responses
  def get(self, url = '/'):
    print "get"
    self.handleRequest()
      
  #~ def post(self, url = '/'):
    #~ print 'post'
    #~ self.handleRequest()

  # handle both GET and POST requests with the same function
  def handleRequest( self ):
    # is op to decide what kind of command is being sent
    #~ op = self.get_argument('', None)
    
    #received a "checkup" operation command from the browser:
    #~ if op == "checkup":
    #make a dictionary
    status = {"server": True, "mostRecentSerial" : json.loads(mostRecentLine) }
    #turn it to JSON and send it to the browser
    self.set_header("Content-Type", 'application/json; charset="utf8"')
    self.write( json.dumps(status) )

# adds event handlers for commands and file requests
application = tornado.web.Application([(r"/(.*)", CommandHandler )])

"""
Convert farenheit to centigrade
"""
def f_to_c(temperature):
  return ((temperature - 32) * (5.0/9.0))
  
"""
Convert centigrade to farenheit
"""
def c_to_f(temperature):
  return ((9.0/5.0) * temperature) + 32

"""
Convert centigrade to kelvin
"""  
def c_to_k(temperature):
  return (temperature + 273.15)
  
"""
Calculates wind chill in degrees Centigrade from a given dry bulb 
temperature and wind speed in km/hr using the Environment Canada model.
(used for all of North America and the UK).
"""
def wind_chill(temperature, windspeed):
  return round(13.12 + (0.6215 * temperature) - (11.37 * 
    (windspeed ** 0.16)) + (0.3965 * temperature * 
    (windspeed ** 0.16)), PRECISION)
    
def heat_index(temperature, humidity): 
  # NOTE: Exposure to direct sunlight can increase heat index as much as 8°C
  temperature_f = c_to_f(temperature) #I couldn't find a purely metric formula
  # Magical weather numbers, or "Sometimes I think they're just guessing"
  c1 = -42.379
  c2 = 2.04901523
  c3 = 10.14333127
  c4 = -0.22475541
  c5 = -0.00683783
  c6 = -0.05481717
  c7 = 1.22874e-3
  c8 = 8.5282e-04
  c9 = -1.99e-06
 
  return round(f_to_c(c1 + c2*temperature_f + c3*humidity + \
    c4*temperature_f*humidity + c5*temperature_f*temperature_f + \
    c6*humidity*humidity + c7*temperature_f*temperature_f*humidity + \
    c8*temperature_f*humidity*humidity + \
    c9*temperature_f*temperature_f*humidity*humidity), PRECISION)

  
def humidex(temperature, humidity):
  #FIXME returns extremely large values
  dewpoint = c_to_k(dew_point(temperature, humidity)) #Dewpoint in Kelvin
  de = 5417.7530 * ((1 / 273.16) - (1 / dewpoint))
  return round(temperature + (0.5555 * (6.11 * math.exp((de)))) - 10, PRECISION)
  
  
def dew_point(temperature, humidity):
  #Constants (1980 paper by David Bolton, see Wikipedia: Dew point)
  a = 6.112 # hPa
  b = 17.67 # ? what is this I don't even
  c = 243.5 # °C
  
  # Took this from a javascript thing: 
  #  http://www.weathercast.co.uk/weather-calculator.html
  # because converting formulas from wikipedia is hard.
  Es = a * pow(10.0, (7.5 * temperature / (c + temperature)));
  E  = (humidity * Es) / 100;

  return round(((-430.22 + 237.7 * math.log(E)) / \
    (-1 * math.log(E) + 19.08) * 10 ) / 10, PRECISION)
  
  
def feels_like(temperature, humidity, windspeed):
  # Wind chill is defined for temperature < 14°C
  # Heat index calculated for temps > 26°C
  # Otherwise neither will make a difference in perceived temperature:
  if temperature <= 14:
    return wind_chill(temperature, windspeed)
  elif temperature >= 26:
    return heat_index(temperature, humidity)
  else:
    return temperature
    
# A dictionary that uses range queries for keys.
# http://joshuakugler.com/archives/30-BetweenDict,-a-Python-dict-for-value-ranges.html
class BetweenDict(dict):
  def __init__(self, d = {}):
    for k,v in d.items():
      self[k] = v

  def __getitem__(self, key):
    for k, v in self.items():
      if k[0] <= key < k[1]:
        return v
    raise KeyError("Key '%s' is not between any values in the BetweenDict" % key)

  def __setitem__(self, key, value):
    try:
      if len(key) == 2:
        if key[0] < key[1]:
          dict.__setitem__(self, (key[0], key[1]), value)
        else:
          raise RuntimeError('First element of a BetweenDict key must be '
                              'strictly less than the second element')
      else:
        raise ValueError('Key of a BetweenDict must be an iterable '
                          'with length two')
    except TypeError:
      raise TypeError('Key of a BetweenDict must be an iterable '
                       'with length two')

  def __contains__(self, key):
    try:
      return bool(self[key]) or True
    except KeyError:
      return False

if __name__ == "__main__":
  ser = serial.Serial(DEVICE, baudrate=9600, timeout=0, writeTimeout=0)
  #tell tornado to run checkSerial every 10ms
  serial_loop = tornado.ioloop.PeriodicCallback(checkSerial, 200)
  serial_loop.start()
  
  #start tornado
  application.listen(PORT)
  print("Starting server on port number %i..." % PORT )
  print("Open at http://127.0.0.1:%i/index.html" % PORT )
  tornado.ioloop.IOLoop.instance().start()
