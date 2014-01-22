#!/usr/bin/env python

class Config(object):
  HOST = "0.0.0.0" #Listen on all interfaces
  
class DevelopmentConfig(Config):
  DEBUG = True
  
