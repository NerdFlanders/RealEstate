import smtplib
import imaplib
import credentials as cd
import email
import email.header
import datetime
import re

def writeMail(receiver):
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

def get_first_text_block(msg):
    type = msg.get_content_maintype()

    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif type == 'text':
        return msg.get_payload()

def readMail():
    IMAP_SERVER = "imap.gmail.com"
    IMAP_PORT   = 993

    readServer = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    readServer.login(cd.gmail_acc, cd.gmail_passwd)

    readServer.select('inbox')
    result, data = readServer.uid('search', None, 'ALL')
    latest_email_uid = data[0].split()[-1]    

    mailCounter = 0
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
            body = get_first_text_block(msg)
            cleanedText = body.replace("\n", "").replace("=\r", "").replace("\r","")
            links = list(re.findall(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=$]*)', cleanedText))
            complete = [] #falsche links, vielleicht fehlendes stück auffüllen mit standart immoscout string
            for i in links:
                if i[0] == 'www.':
                    complete.append( i[0] + i[1] )

            if links.count != 0:
                link = links.group()
                countGroup = links.group().count
                group = []
                for i in links:
                    group.append(i)
                    print(i)
                firstLink = link.replace('Scout-ID:',"")
                if "expose" in firstLink:
                    print(firstLink)
            # print(cleanedText)
            # print("\n\n\n")
            # print(repr(body))
            # print ('Message %s: %s' % (curmail, subject))
            # print ('Raw Date:', msg['Date'])
            mailCounter += 1;
            #print(mailCounter)
            # Now convert to local date-time
            date_tuple = email.utils.parsedate_tz(msg['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(
                    email.utils.mktime_tz(date_tuple))
                #print ("Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S"))

    
    # raw_email = data[0][1]
    # #print(raw_email)
    # print(type(raw_email))
    # print(raw_email.decode("utf-8"))
    


readMail()


