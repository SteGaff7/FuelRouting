import math
import csv
import urllib.request
import json

from Airport import Airport
from todays_currency_rates import todays_currency_rates

class atlas():
    __airport_dict = {}
    __distance_matrix = {}
    __weighted_matrix = {}
    
    @classmethod
    def update(cls,route_list):
        
        #Airport Dict
        
        #Check that each airport in route has been created as an airport object if not create and add to dict
        for airport_code in route_list:
            #If airport_code not in dictionary then create an airport object and add airport_code as key to dict
            if airport_code not in cls.get_airport_dict():
                
                try:
                    csv_file = csv.reader(open('airport.csv', 'r'), delimiter=",")
                    for row in csv_file:
                        #Match code to equivalent row in CSV file and attain relevant data
                        if airport_code == str(row[4]):
                            cls.add_airport(airport_code,row[2],row[3],float(row[6]),float(row[7]))
                            
                except error as e:
                    print(e)
    
    
    
        #Distance Matrix
       
        #Check that each airport in list is in distance matrix dict and has a dict-matrix with each other airport in list
        for code in route_list:

            #If not in dict, create new nested dict to distance to each other airport
            if code not in cls.get_distance_matrix():
                sub_dist_dict = {}
                for code2 in route_list:
                    try:
                        #Use destination airport as key to inner nested dictionary in matrix
                        sub_dist_dict[code2] =  (cls.get_airport(code)).distance_between(cls.get_airport(code2))
                        
                    except:
                        print("Error: between:", code, code2)
                        #print(self.airport_dict[code].distance_between(self.airport_dict[code2]))
                        
                #Use departing airport as key to outer dictionary in matrix
                cls.add_distance(code, sub_dist_dict)

            #If airport is already a key in dictionary
            else:
                sub_dist_dict = {}
                for code2 in route_list:
                    #Add the other airports to the existing inner dict if they are not already part of it
                    if code2 not in cls.get_sub_distance_matrix(code):
                        try:
                            sub_dist_dict[code2] = (cls.get_airport(code)).distance_between(cls.get_airport(code2))
                        except:
                            print("Error: between:", code, code2)  
                            
                cls.append_sub_dict(code, sub_dist_dict)
        
        
        
        #Weighted Matrix
        
        #Create a dictionary for the weighted matrix based on todays currency rates
    
        #Same methodology from distance matrix above
        for code in route_list:
            if code not in cls.get_weight_matrix():
                cost_dict = {}
                for code2 in route_list:
                    try:
                        cost_dict[code2] = round((cls.get_distance_between(code, code2))*\
                                                 (cls.get_airport(code).get_currencyToday()),2)
                    except:
                        print("Error in weighted matrix between", code, code2)
                        
                #Add cost dictionary as the value to the airport_code as they key to the weighted_matrix       
                cls.add_weight(code, cost_dict)

            #If airport is already a key in dictionary
            else:
                cost_dict = {}
                for code2 in route_list:
                    if code2 not in cls.get_sub_weighted_matrix(code):
                        try:
                            cost_dict[code2] = round((cls.get_distance_between(code, code2))*\
                                                 (cls.get_airport(code).get_currencyToday()),2)
                        except:
                            print("Error in weighted matrix between", code, code2)
                            
                cls.append_sub_weight_dict(code, cost_dict)
     
    
        
    #Airport dict - Create a dictionary of Airport Codes : Actual Airport instances(objects) using Airport() Class
    @classmethod
    def add_airport(cls, airport_code, name, country, lat, long ):
        cls.__airport_dict[airport_code] = Airport(airport_code, name, country, lat, long)
    
    @classmethod
    def get_airport(cls, airport_code):
        return cls.__airport_dict[airport_code]
    
    @classmethod
    def get_airport_dict(cls):
        return cls.__airport_dict
    
    @classmethod
    def print_airport_dict(cls):
        for airport in cls.get_airport_dict():
            print(airport + " - " + str(cls.get_airport(airport)))
    
    
    
    #Dist Dict Methods
    @classmethod
    def add_distance(cls, airport_code, sub_dict):
        cls.__distance_matrix[airport_code] = sub_dict
        
    @classmethod
    def append_sub_dict(cls, airport_code, sub_dict):
        cls.__distance_matrix[airport_code].update(sub_dict)
        
    @classmethod
    def get_distance_matrix(cls):
        return cls.__distance_matrix
    
    @classmethod
    def get_sub_distance_matrix(cls, code):
        return cls.get_distance_matrix()[code]
    
    @classmethod
    def get_distance_between(cls, airport_code, to_airport):
        return cls.get_sub_distance_matrix(airport_code)[to_airport]
    
    @classmethod
    def print_distance_matrix(cls):
        print("DISTANCE MATRIX" + "\n************************************")
        for start_airport in cls.get_distance_matrix():
            print("DISTANCE FROM " + start_airport + " TO:")
            for dest_airport in cls.get_sub_distance_matrix(start_airport):
                print("\t"+dest_airport, str(cls.get_sub_distance_matrix(start_airport)[dest_airport]) + "km")
            print()
        print("END" + "\n************************************")
    
    
    
    #Weighted Dict Methods
    @classmethod
    def add_weight(cls, airport_code, sub_dict):
        cls.__weighted_matrix[airport_code] = sub_dict
    
    @classmethod
    def append_sub_weight_dict(cls, airport_code, sub_dict):
        cls.__weighted_matrix[airport_code].update(sub_dict)
        
    @classmethod
    def get_weight_matrix(cls):
        return cls.__weighted_matrix
    
    @classmethod
    def get_sub_weighted_matrix(cls, code):
        return cls.get_weight_matrix()[code]
    
    @classmethod
    def get_price_between(cls, airport_code, to_airport):
        return cls.get_sub_weighted_matrix(airport_code)[to_airport]
    
    @classmethod
    def print_weighed_matrix(cls):
        print("WEIGHTED MATRIX" + "\n************************************")
        for start_airport in cls.get_weight_matrix():
            print("PRICE FROM " + start_airport + " TO:")
            for dest_airport in cls.get_sub_weighted_matrix(start_airport):
                print("\t"+dest_airport, str(cls.get_sub_weighted_matrix(start_airport)[dest_airport]) + "e")
            print()
        print("END" + "\n************************************")