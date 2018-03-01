import smtplib
import imaplib
import credentials as cd
import email
import email.header
import datetime
import re
import logging
from bs4 import BeautifulSoup
from urllib.request import urlopen

logging.basicConfig(level=logging.DEBUG)
logging.disable(logging.CRITICAL)

class mailreader:
    def __init__(self):
        logging.debug("mailreader created")
      
    
    def readMail(self, test):        
        IMAP_SERVER = "imap.gmail.com"
        IMAP_PORT   = 993

        readServer = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        readServer.login(cd.gmail_acc, cd.gmail_passwd)

        readServer.select('inbox')
        result, data = readServer.uid('search', None, '(UNSEEN)')
        latest_email_uid = data[0].split()[-1]    

        allLinksToExpose = []

        for curmail in data[0].split():
            
            result, data = readServer.uid('fetch', curmail, '(RFC822)')

            msg = email.message_from_string(data[0][1].decode("utf-8", errors="ignore"))
            decodedMail = email.header.decode_header(msg['Subject'])[0]
            
            subject = ""
            if type(decodedMail[0]) == bytes:
                subject = decodedMail[0].decode("utf-8")
            else:
                subject = decodedMail[0]
            
            if "Eigentumswohnung" in subject:
                body = self.__get_first_text_block(msg)
                cleanedText = body.replace("\n", "").replace("=\r", "").replace("\r","")
                links = list(re.findall(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=$]*)', cleanedText))
                
                complete = self.__getExposeLinks(links)
                logging.debug(complete)
                allLinksToExpose.append(complete)
                
        return allLinksToExpose


    def getLinksFromSearch(self, typ, county, city ):
        countPages = self.__getPageNumber("https://www.immobilienscout24.de/Suche/S-T/"+ typ +"/"+ county +"/"+ city)
        linksToObj = []
        for i in range(1, countPages+1):
            obj = "https://www.immobilienscout24.de/Suche/S-T/P-"+ str(i) +"/"+ typ +"/"+ county +"/"+ city
            try:
                #todo
                page = urlopen(obj)
            except:
                print("exteion occured")
                continue
            parsed = BeautifulSoup(page, 'html.parser')

            # if(countPages == 1 and start == True):                
            #     start = False
            
            exposes = []
            pattern = re.compile('\/expose\/[1-9]+')
            patternis24 = re.compile(r'is24')
            links = parsed.findAll('a', href=True)
            for a in links:
                if(pattern.match(a['href']) and len(a['href']) <= 18):
                    exposes.append(a['href'])
                    print(a['href'])
            
            linksToObj.append(list(set(exposes)))

            print(linksToObj)
        return linksToObj


    def __getExposeLinks(self,links):
        complete = []
        for i in links:
            if i[0] == 'www.' and 'expose' in i[1] and 'redirecttocontactform' not in i[1]:
                exposeLink = "https://" + i[0] + "immobilienscout24.de" + i[1][:17]
                if exposeLink not in complete:
                    complete.append( exposeLink )
        return complete

    def __get_first_text_block(self,msg):
            type = msg.get_content_maintype()

            if type == 'multipart':
                for part in msg.get_payload():
                    if part.get_content_maintype() == 'text':
                        return part.get_payload()
            elif type == 'text':
                return msg.get_payload()  
    
    def __getPageNumber(self, obj):
        try:
            page = urlopen(obj)
        except:
            print("exeption occured")

        parsed = BeautifulSoup(page, 'html.parser')
        countPages = 1
        selector = parsed.find_all(class_='select font-standard')
        print(selector.count)
        if(selector != []):
            for option in selector[0].contents:
                foundPages = option['value']
                countPages = int(foundPages.replace("'", ""))
        return countPages
    

# mr = mailreader()
# mr.getLinksFromSearch("Wohnung-Kauf","Bayern","Nuernberg")


