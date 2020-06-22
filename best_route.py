import math
import csv
import urllib.request
import json

from atlas import atlas
from aircraft_roster import aircraft_roster

#Class that returns best route and price
class best_route():    
    
    def __init__(self, airportsToVisit, plane_code):
        try:
            if airportsToVisit[0]!=airportsToVisit[-1]:
                airportsToVisit.append(airportsToVisit[0])
            test=airportsToVisit[1:-1]
            for airport in test:
                count=0
                for airports in test:
                    if airport==airports:
                        count+=1
                if count>1:
                    raise ValueError("You have a duplicate airport within your flight list. \nThe only duplicate airport allowed is your home and destination airport.")
            self.__allRoutes=self.__recur(airportsToVisit,0, plane_code)
            self.__bestRoute=self.__cheapest_route(self.__allRoutes)
        except ValueError as e:
            print(e)

    #recurssive function that returns a list of the prices and routes of each possible combination   
    def __recur(self, myList, i, plane_code):
        #needed to calculate the number of routes in a branch below the current
        def fact(n, a): 
            if (n == 0):
                return a 
            return fact(n - 1, n * a)  
        #create a new list without the start airport for each trip
        total = 0
        working = myList[i]
        currentList = myList.copy()
        currentList.remove(working)

        #base case of recurssive function, e.g last trip of the journey, when only two possible airports remaining
        if len(myList) == 2:
            #holds the total price of trip calculated in the first list. Holds the airport codes it has travelled to in the second. 
            totals = [[],[]]
            totals[1].append(working+'-'+currentList[0])
            #if the plane cannot make the trip add False to the list instead of the price and airport code.
            if atlas.get_distance_between(working, currentList[0])>aircraft_roster.access_aircraft(plane_code).max_range:
                totals[0].append(False)
            else:
                price = atlas.get_price_between(working, currentList[0])
                totals[0].append(price)

        else:
            totals = [[],[]]
            #List of all other airports except departing airport and home airport
            for j in range(0,len(currentList)-1,+1):
                #Check to see if distance is within the plane range
                #if the plane cannot make the trip, there is no need to enter the recursive function to calculate
                #the routes below as we know the plane can't take that route.
                #By finding the factorial of the currentlist-2 you add the correct amount of False values 
                #to the list instead of the prices and airport codes.
                if atlas.get_distance_between(working, currentList[j])>aircraft_roster.access_aircraft(plane_code).max_range:
                    #print(working,"",currentList[j], "is impossible")
                    for k in range(0, fact(len(currentList)-2, 1)):
                        totals[0].append(False)
                        totals[1].append('False')
                else:
                    price = atlas.get_price_between(working, currentList[j])
                    #print(working,"",currentList[j], "is possible")
                    #x will hold the totals lists containing all possible routes and corresponding prices
                    #down the tree from this airport.
                    x=self.__recur(currentList, j, plane_code)
                    for index in range(0, len(x[0])):
                        #k represents each price in the totals list from the trees below.
                        #if a branch below cannot be flown i.e price==False, the whole route must be false
                        if x[0][index]==False:
                            totals[0].append(False)
                            totals[1].append('False')
                        else:
                            #Adds the cost of the flights between the airports in the brances below 
                            #to the cost between the airports at this level
                            total = x[0][index] + price
                            #Adds the airport code of the airports flown in the brances below 
                            #to the current airport code
                            route = working +'-'+x[1][index]
                            #Add each possible combination to this airports list of possible combinations/tree
                            totals[0].append(total)
                            totals[1].append(route)
        #print(totals)
        return totals
    
    def display_allRoutes(self):
        for route in range(0, len(self.__allRoutes[0])):
            print(str(self.__allRoutes[1][route])+" : "+str(self.__allRoutes[0][route]))
            print()
    
    #Calcualtes the cheapest route using the mapped dictionary
    def __cheapest_route(self, mappedDict):  
        bestPrice = mappedDict[0][0]
        bestRoute = mappedDict[1][0]
        #Access list by index and compare price to min price and reassign accordingly

        for index in range(0, len(mappedDict[0])):
            #if bestPrice is false, replace with first non False price
            if bestPrice==False and mappedDict[0][index] != False:
                bestPrice = mappedDict[0][index]
                bestRoute = mappedDict[1][index]                
                                
            #if mappedDict[key][Price]not equal to false and bestPrice not equal to False, compare
            elif bestPrice!=False and mappedDict[0][index] != False:
                if mappedDict[0][index] < bestPrice:
                    bestPrice = mappedDict[0][index]
                    bestRoute = mappedDict[1][index]

        if bestPrice==False:
            return "There is no route that this plane can complete with it's fuel limitation"
        return str(bestRoute) + " is the cheapest route and costs " + str(bestPrice) + "."
    
    def get_cheapestRoute(self):
        return self.__bestRoute