from getLinksService import mailreader as mr
from webparser import webparser as wp

def main():
    allMails = mr()
    #exposeLinkList = allMails.__readMail__("test")
    exposeLinkList = allMails.getLinksFromSearch("Wohnung-Miete","Bayern","Nuernberg")
    parser = wp()
    allAttributes = parser.getInfoFromExpose(exposeLinkList)
    parser.writePropertiesToDB(allAttributes)
    #sendMailsToSubscribers(exposeProperties)

if __name__ == "__main__":
    main()

#Wohnung-Kauf
#Wohnung-Miete