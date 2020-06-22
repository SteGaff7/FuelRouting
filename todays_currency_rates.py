import math
import csv
import urllib.request
import json
#Creating a currency rate class for that day (optional as a class or global dict?)
#Using an API to get daily rates
#Dictionary of key "CurrencyCode" : value "TodaysExchangeRate"
class todays_currency_rates():
    currency_code_rates_dict = {}
    with urllib.request.urlopen("http://data.fixer.io/api/latest?access_key=340fa686ffcff7fdb67e23b57b246b8a") as url:
        data = json.loads(url.read().decode())
        for currency in data['rates']:
            currency_code_rates_dict[currency] = data['rates'][currency]
    
    #If there are any currencies that the API does not pick up then add as key from the CSV file provided
    with open('currencyrates.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        csvfile.readline()   # skip the first line
        for row in readCSV:
            if row[1] not in currency_code_rates_dict:
                currency_code_rates_dict[row[1]] = float(row[3])