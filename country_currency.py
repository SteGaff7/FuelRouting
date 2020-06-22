import math
import csv
import urllib.request
import json
#Creating a dictionary of country names to the currency code from file "itu.csv"
#Dictionary of key "Country" : value "CurrencyCode"
#Static data that does not change hence ???not implemented as a class
class country_currency():
    country_currency_code_dict = {}
    with open('countrycurrency.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        csvfile.readline()   # skip the first line
        for row in readCSV:
            country_currency_code_dict[row[0]] = row[14]