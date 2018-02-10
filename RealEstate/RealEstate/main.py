from getLinksService import mailreader as mr

def main():
    allMails = mr()
    allMails.__readMail__("test")

if __name__ == "__main__":
    main()