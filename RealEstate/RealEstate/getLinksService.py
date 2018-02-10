import smtplib
import imaplib
import credentials as cd
import email
import email.header
import datetime
import re
import logging

logging.basicConfig(level=logging.DEBUG)
logging.disable(logging.CRITICAL)

class mailreader:
    def __init__(self):
        logging.debug("mailreader created")
        
    def __writeMail(self,receiver):
        TO = 'jenja.dietrich@gmail.com' #replace by reciver
        SUBJECT = 'TEST MAIL'
        TEXT = 'Here is a message from python.'

        SMTP_SERVER = "imap.gmail.com"
        SMTP_PORT   = 993

        # Gmail Sign In
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(cd.gmail_acc, cd.gmail_passwd)

        BODY = '\r\n'.join(['To: %s' % TO,
                            'From: %s' % gmail_sender,
                            'Subject: %s' % SUBJECT,
                            '', TEXT])

        try:
            #server.sendmail(gmail_sender, [TO], BODY)
            print ('fake email sent')
        except:
            print ('error sending mail')

        server.quit()

    def __readMail__(self, test):        
        IMAP_SERVER = "imap.gmail.com"
        IMAP_PORT   = 993

        readServer = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        readServer.login(cd.gmail_acc, cd.gmail_passwd)

        readServer.select('inbox')
        result, data = readServer.uid('search', None, 'ALL')
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
                logging.debug(complete + "\n")
                allLinksToExpose.append(complete)
                
        return allLinksToExpose


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
    
    

#readMail()

