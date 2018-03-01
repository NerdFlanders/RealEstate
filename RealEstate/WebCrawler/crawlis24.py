from dal import sql
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time, sched

def crawl():
    s = sched.scheduler(time.time, time.sleep)
    startRange = 45278467
    lastId = accessToFile(startRange, 0)
    
    if(lastId != ''):
        startRange = int(lastId)

    for exposeId in range(startRange, 99999999999): #99.999.999.999  
        is24 = "https://www.immobilienscout24.de/expose/" + str(exposeId)

        try:            
            s.enter(10, 1, accessToFile, (exposeId, 1,)) 
            page = urlopen(is24)            
            if(page.status == 200):
                writeToDB(page, exposeId)
        except:
            print("page %s not available", exposeId)
            continue

def writeToDB(page, exposeId):
    parsed = BeautifulSoup(page, 'html.parser')

    exposeType = ""
    dictType = {
        "Wohnung mieten": "RentFlat",
        "Wohnung kaufen": "BuyFlat",
        "Haus kaufen": "ByHouse",
        "Haus mieten": "RentHouse"
    }
    foundType = parsed.find(class_="breadcrumb__link margin-horizontal-xs")
    typeObj = dictType.get(foundType.contents[0])
 
    dateCreated = time.strftime("%d/%m/%Y")
    
    priceObj = parsed.find(class_="is24qa-kaltmiete is24-value font-semibold")
    
    if(priceObj == None):
        priceObj = parsed.find(class_="is24qa-kaufpreis is24-value font-semibold")
    price = int(priceObj.contents[0].replace(".", "").replace("€", "").strip())

    locationObj = parsed.find(class_="zip-region-and-country")
    location = locationObj.contents[0].strip()

    sqlObj = sql() 
    print(type(exposeId))
    print(type(dateCreated))
    print(type(typeObj))
    print(type(price))
    print(type(location))
    sqlObj.writeExposeToDB(exposeId, dateCreated, typeObj, price, location)
    print ("entry added")

def accessToFile(exposeId, mode):
    if(mode == 1):
        file = open('stoppPoint.dat', 'a+')
        file.writelines(exposeId)
    
    if(mode == 0):
        try:
            file = open('stoppPoint.dat', 'r')
        except IOError:
            file = open('stoppPoint.dat', 'w')
        latestExpose = file.read(-1)
        return latestExpose
crawl()