import pymysql
import credentials as cd

class sql:
    def __init__(self, *args, **kwargs):
        self.db = pymysql.connect("localhost",cd.db_acc,cd.db_passwd,"realestates" )

        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()

        # execute SQL query using execute() method.
        self.cursor.execute("create TABLE IF NOT EXISTs Subscribers (id int(8) unsigned auto_increment PRIMARY KEY, Mailaddress varchar(100) not null)")
        self.cursor.execute("""create TABLE IF NOT EXISTs Exposes (
                                    id int(8) unsigned auto_increment PRIMARY KEY, 
                                    ExposeId int not null, 
                                    DateCreated varchar(10) not null, 
                                    Type varchar(30), 
                                    Price int null, 
                                    Location varchar(50) not null,
                                    Rooms int null,
                                    Area int null,
                                    GeneralType varchar(50) null)""")

    def getSubscribers(self):
        # Fetch a single row using fetchone() method.
        self.cursor.execute("select mailaddress FROM Subscribers")
        
        data = self.cursor.fetchone()
        #print ("Database version : %s " % data)

        # disconnect from server
        self.db.close()
        return data

        
    def writeExposeToDB(self, exposeId, dateCreated, typeObj, price, location, rooms, area, generalType):
        self.cursor.execute("""insert into Exposes (
                                                    ExposeId, 
                                                    DateCreated, 
                                                    Type, 
                                                    Price, 
                                                    Location,
                                                    Rooms,
                                                    Area,
                                                    GeneralType) 
                                            values (%s,%s,%s,%s,%s,%s,%s,%s)""", (exposeId, dateCreated, typeObj, price, location, rooms, area, generalType))        
        result = self.db.commit()
        print("Added to database %s: %s" % (exposeId, result))

