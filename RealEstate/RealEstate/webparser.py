from bs4 import BeautifulSoup
from urllib.request import urlopen
import logging
import re
from dal import sql
import time

logging.basicConfig(level=logging.DEBUG)
logging.disable(logging.CRITICAL)

class webparser():
    
    def __init__(self):
        logging.debug("initialized")

    def getInfoFromExpose(self, webLinks):
        propertiesOfAll = []
        for links in webLinks:
            for obj in links:
                exposeObj = {}

                if(obj[:7] == '/expose'):
                    obj = "https://www.immobilienscout24.de" + obj

                try:
                    print("Try parsing expose: %s" % obj)
                    page = urlopen(obj)
                except:
                    continue
                parsed = BeautifulSoup(page, 'html.parser')

                #get all important values
                notFound = parsed.find(class_="not-found")
                if (notFound != None):
                    continue

                priceObj = parsed.find(class_="is24qa-kaufpreis is24-value font-semibold")
                rentObj = parsed.find(class_="is24qa-kaltmiete is24-value font-semibold")
                roomsObj = parsed.find(class_="is24qa-zi is24-value font-semibold")
                areaObj  = parsed.find(class_="is24qa-wohnflaeche-ca is24-value font-semibold")
                rentAreaObj  = parsed.find(class_="is24qa-flaeche is24-value font-semibold")
                typeObj  = parsed.find(class_="is24qa-typ grid-item three-fifths")
                featuresObj = parsed.find(class_="criteriagroup boolean-listing padding-top-l")
                locationObj = parsed.find(class_="zip-region-and-country")
                dictType = {
                    "Wohnung mieten": "RentFlat",
                    "Wohnung kaufen": "BuyFlat",
                    "Haus kaufen": "ByHouse",
                    "Haus mieten": "RentHouse"
                }
                foundType = parsed.find(class_="breadcrumb__link margin-horizontal-xs")
                generalType = dictType.get(foundType.contents[0])
                                
                featuresList = []
                if(featuresObj != None):
                    for labels in featuresObj:
                        try:
                            if labels.text != None and labels.getText() != "":
                                #print(type(labels))
                                featuresList.append(labels.getText())                          
                        except Exception as e:
                            pass
                            #print('Error: '+ str(e))
                else:
                    featuresList.append("None")
                
                exposeObj['features'] = featuresList

                price = self.checkAttribute(priceObj)
                rent = self.checkAttribute(rentObj)
                rooms = roomsObj.contents[0].strip() 
                area = self.checkAttribute(areaObj)
                rentArea = self.checkAttribute(rentAreaObj)
                objectType = self.checkAttribute(typeObj)

                rawPrice = 0;
                if(price != 'None'):                    
                    rawPrice= int(price.split(" ")[0].replace(".", "").replace(",", "."))
                elif (rent != 'None'):
                    rawPrice= int(round(float(rent.split(" ")[0].replace(".", "").replace(",", ".")),0))

                livingArea = 'None'
                if(area != 'None'):
                    livingArea = area
                elif(rentArea != 'None'):
                    livingArea = rentArea

                finalArea = int(livingArea.split(" ")[0].split(",")[0])
                ppsqm = round(rawPrice / finalArea, 2)
                location = self.checkAttribute(locationObj)

                rent = 500
                months = 12
                yearsToPayBack = rawPrice / rent / months

                exposeObj['id'] = obj.split("/")[-1]
                exposeObj['price'] = rawPrice
                exposeObj['rooms'] = rooms
                exposeObj['area'] = area
                exposeObj['type'] = objectType
                exposeObj['breakeven'] = yearsToPayBack
                exposeObj['ppsqm'] = ppsqm
                exposeObj['Date'] = time.strftime("%d/%m/%Y")
                exposeObj['location'] = location
                exposeObj['area'] = finalArea
                exposeObj['generalType'] = generalType
                
                #print(exposeObj)
                propertiesOfAll.append(exposeObj)
                print("Got properties from %s" % obj)
        return propertiesOfAll    

    def writePropertiesToDB(self, allExposeWithProperties):
        sqlObj = sql() 

        for expose in allExposeWithProperties:
            sqlObj.writeExposeToDB(expose.get('id'), expose.get('Date'), expose.get('type'), expose.get('price'), expose.get('location'), expose.get('rooms'), expose.get('area'),expose.get('generalType') )

    def checkAttribute(self, attr):
        value = ""
        try:
            value = attr.contents[0].strip()
        except:
            value = "None"
        return value
    
# links = [["https://www.immobilienscout24.de/expose/100716312"]]
# w = webparser()
# expList = w.getInfoFromExpose(links)
# w.writePropertiesToDB(expList)

