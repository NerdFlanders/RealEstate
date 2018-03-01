from dal import sql
import smtplib
import imaplib
import credentials as cd
import email
import email.header

class mailSender:
    def __init__(self, *args, **kwargs):
        return

    def sendMailToSubscribers(self):
        dbCon = sql()
        subscribers = dbCon.getSubscribers()
        for subscriber in subscribers:
            self.__writeMail(subscriber)

    def __writeMail(self, receiver):
        TO = receiver 
        SUBJECT = 'TEST MAIL'
        TEXT = 'Here is a message from python.'

        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT   = 587 #993

        # Gmail Sign In
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(cd.gmail_acc, cd.gmail_passwd)

        BODY = '\r\n'.join(['To: %s' % TO,
                            'From: %s' % cd.gmail_acc,
                            'Subject: %s' % SUBJECT,
                            '', TEXT])

        try:
            server.sendmail(cd.gmail_acc, [TO], BODY)
            print ('email sent')
        except:
            print ('error sending mail')

        server.quit()


ms = mailSender()
ms.sendMailToSubscribers()