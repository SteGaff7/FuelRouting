import math
import csv
import urllib.request
import json

class aircraft():
    def __init__ (self, code, max_range):
        self.code = code
        self.max_range = max_range
    @property
    def code(self):
        return self.__code
    @code.setter
    def code(self, code):
        self.__code=code
    @property
    def max_range(self):
        return self.__max_range
    @max_range.setter
    def max_range(self, max_range):
        self.__max_range=max_range
    def display_aircraft(self):
        return('Code: '+self.code+". Max Range: "+str(self.max_range))