import math
import csv
import urllib.request
import json

from aircraft import aircraft

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

class aircraft_roster():
    __aircraft_dict = {}
    with open('aircraft.csv') as __csvfile:
        __readCSV = csv.reader(__csvfile, delimiter=',')
        __csvfile.readline() #Skip first line
        for __row in __readCSV:
            #aircraft_dict[row[3]+" "+row[0]] = row[4]
            __aircraft_dict[__row[0]] = aircraft(__row[0], int(__row[4]))
    def __init__(self, name):
        self.name=name
    @classmethod
    def __get_aircraftDict(cls):
        return cls.__aircraft_dict
    @classmethod
    def access_aircraft(cls, code):
        if code in cls.__aircraft_dict:
            return cls.__aircraft_dict[code]
        else:
            print('That aircraft is not currently part of the roster.')
    @classmethod        
    def add_aircraft(cls, code, max_range):
        if code not in cls.__aircraft_dict:
            cls.__aircraft_dict[code] = aircraft(code, int(max_range))
        else:
            print('That aircraft is already part of the roster.')
    @classmethod
    def remove(cls, code):
        if code in cls.__aircraft_dict:
            cls.__aircraft_dict.pop(code)
        else:
            print('That aircraft is not currently part of the roster.')
    @classmethod
    def display_roster(cls):
        __a=aircraft_roster.__get_aircraftDict()
        for plane in __a:
            print(__a[plane].display_aircraft())
    @classmethod
    def update_aircraft_max_range(cls, code, new_range):
        if code in cls.__aircraft_dict:
            aircraft_roster.access_aircraft(code).max_range=new_range
        else:
            print('That aircraft is not currently part of the roster.')     