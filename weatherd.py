#!/usr/bin/env python
#*-* coding: utf8 *-*

from twisted.internet import defer, reactor
import math

PRECISION = 1 # Round to one decimal place for derivative calculations

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
  return (temperature - 273.15)
  
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
  return round(temperature + (0.5555 * (6.11 * math.e ** (de))) - 10, PRECISION)
  
  
def dew_point(temperature, humidity):
  #Constants (1980 paper by David Bolton, see Wikipedia: Dew point)
  a = 6.112 # hPa
  b = 17.67 # ? what is this I don't even
  c = 243.5 # °C
  
  # Took this from a javascript thing: http://www.weathercast.co.uk/weather-calculator.html
  # because converting formulas from wikipedia is hard.
  Es = a * pow(10.0, (7.5 * temperature / (c + temperature)));
  E  = (humidity * Es) / 100;

  return round(((-430.22 + 237.7 * math.log(E)) / \
    (-1 * math.log(E) + 19.08) * 10 ) / 10, PRECISION)
  
  
def feels_like(temperature, humidity, windspeed):
  # Wind chill is defined for temperature < 14°C
  # Heat index calculated for temps > 26°C
  # Not sure what to do with the interval between 14 and 26.
  pass
