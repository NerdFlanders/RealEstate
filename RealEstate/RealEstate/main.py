from getLinksService import mailreader as mr

def main():
    allMails = mr()
    exposeProperties = allMails.__readMail__("test")
    #sendMailsToSubscribers(exposeProperties)

if __name__ == "__main__":
    main()