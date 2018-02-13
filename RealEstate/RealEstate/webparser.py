from bs4 import BeautifulSoup
from urllib.request import urlopen
import logging
import re

logging.basicConfig(level=logging.DEBUG)
logging.disable(logging.CRITICAL)

class webparser():
    
    def __init__(self, webLinks):
        self.links = webLinks

    def getInfoFromExpose(self):
        
        for link in self.links:
            exposeObj = {}

            page = urlopen(link)
            parsed = BeautifulSoup(page, 'html.parser')

            #get all important values
            priceObj = parsed.find(class_="is24qa-kaufpreis is24-value font-semibold")
            roomsObj = parsed.find(class_="is24qa-zi is24-value font-semibold")
            areaObj  = parsed.find(class_="is24qa-wohnflaeche-ca is24-value font-semibold")
            typeObj  = parsed.find(class_="is24qa-typ grid-item three-fifths")
            placeObj = parsed.find(class_="zip-region-and-country")
            featuresObj = parsed.find(class_="criteriagroup boolean-listing padding-top-l")

            featuresList = []
            for labels in featuresObj:
                try:
                    if labels.text != None and labels.getText() != "":
                        #print(type(labels))
                        featuresList.append(labels.getText())                          
                except Exception as e:
                    print('Error: '+ str(e))
            
            exposeObj['features'] = featuresList

            price = priceObj.contents[0].strip() 
            rooms = roomsObj.contents[0].strip() 
            area = areaObj.contents[0].strip() 
            objectType = typeObj.contents[0].strip()
            place = placeObj.contents[0].strip()
            rawPrice= int(price.split(" ")[0].replace(".", ""))
            ppsqm = round(rawPrice / int(area.split(" ")[0]), 2)

            rent = 500
            months = 12
            yearsToPayBack = rawPrice / rent / months

            exposeObj['Price'] = price
            exposeObj['rooms'] = rooms
            exposeObj['area'] = area
            exposeObj['type'] = objectType
            exposeObj['breakeven'] = yearsToPayBack

            print(exposeObj)
            return exposeObj

    
links = ["https://www.immobilienscout24.de/expose/102924216"]
w = webparser(links)
w.getInfoFromExpose()

