import pymysql

class sql:
    def __init__(self, *args, **kwargs):
        self.db = pymysql.connect("localhost","","","realestates" )

        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()

        # execute SQL query using execute() method.
        self.cursor.execute("create TABLE IF NOT EXISTs Subscribers (id int(8) unsigned auto_increment PRIMARY KEY, Mailaddress varchar(100) not null)")

    def getSubscribers(self):
        # Fetch a single row using fetchone() method.
        self.cursor.execute("select mailaddress FROM Subscribers")
        
        data = self.cursor.fetchone()
        #print ("Database version : %s " % data)

        # disconnect from server
        self.db.close()
        return data

test = sql()
subs = test.getSubscribers()
print(subs)