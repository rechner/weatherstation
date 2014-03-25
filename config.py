#!/usr/bin/env python

class Config(object):
  DATA_SOURCE = "localhost:8000"
  HOST = "0.0.0.0" #Listen on all interfaces
  
class DevelopmentConfig(Config):
  DEBUG = True
  
