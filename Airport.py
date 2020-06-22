import math
import csv
import urllib.request
import json

from country_currency import country_currency
from todays_currency_rates import todays_currency_rates

#Airport class that will be created by the Atlas class once the file of airports is provided
class Airport():
    def __init__(self, code="", name="", country="", lat=0, long=0):
        self.set_code(code)
        self.set_name(name)
        self.set_country(country)
        self.set_long(long)
        self.set_lat(lat)
        self.set_radlong(long)
        self.set_radlat(lat)
        self.set_currencyCode()
    
    def set_code(self, code):
        
        codeList=[]
     
        csv_file = csv.reader(open('airport.csv', 'r'), delimiter=",")
        for row in csv_file:
            codeList.append(str(row[4]))
        
        if code not in codeList:
            print("Error- code not valid")
        else:
            self._code = code
    
    def set_name(self, name):
         #No error checking for name as name may contain abbreviations. Also code will uniquely identify airports rather than name     
        self._name=name
    
    def set_country(self,country):
        if country not in country_currency.country_currency_code_dict:
            print("Error- country not valid")
        else:
            self._country = country
    
    def set_long(self,long):
        
        if long >180 or long <-180:
            print("Invalid longitude entered")
        else:
            self._long = long
            
    
    def set_lat(self,lat):
        
        if lat >90 or lat <-90:
            print("Invalid latitude entered")
        else:
            self._lat = lat
           
    
    def set_radlong(self,long):
        self._radlong = self.radians(long)
        
    def set_radlat(self,lat):
         self._radlat = self.radians(lat)    
    
    def set_currencyCode(self):
        try:
            #Index the country currency code dict using the country as the key
            self._currencyCode = country_currency.country_currency_code_dict[self.get_country()]
        except:
            #If currency is not specified automatically default to USD
            self._currencyCode = country_currency.country_currency_code_dict["United States"]
    
    
    def get_code(self):
        return self._code
    
    def get_name(self):
        return self._name
    
    def get_country(self):
        return self._country
    
    def get_long(self):
        return self._long
    
    def get_lat(self):
        return self._lat
    
    def get_radlong(self):
        return self._radlong
    
    def get_radlat(self):
        return self._radlat
    
    def get_currencyCode(self):
        return self._currencyCode
    
    
    #Method that returns the absolute Great Circular Distance between two airports
    def distance_between(self, airport_code):
        #Getting radian equivalent of 90 degrees
        rad90 = self.radians(90)
        
        
        argument_to_acos = (math.sin(rad90-self.get_radlat())*math.sin(rad90-airport_code.get_radlat())*\
        math.cos(self.get_radlong()-airport_code.get_radlong()))+(math.cos(rad90-self.get_radlat())*\
        math.cos(rad90-airport_code.get_radlat()))
        
        #To take care of floating point number 1.0000000002... Cannot get math.acos of > 1!
        if argument_to_acos > 1:
            argument_to_acos = 1
        distance = (math.acos(argument_to_acos))*6371
        return round(abs(distance), 0)
    
    #method that will return the actual numeric value of the currency at todays rate
    #indexes the Today instance of CurrencyRate class using the currencyCode
    def get_currencyToday(self):
        try:
            #Index the todays currency rates dict using the currency code as the key
            return todays_currency_rates.currency_code_rates_dict[self.get_currencyCode()]
        except:
            #If the currency code does not exist on the API or the CSV file then return the USD as the currency
            return todays_currency_rates.currency_code_rates_dict["USD"]
        
    def radians(self, degrees):
        radians = degrees*((math.pi)/180)
        return radians