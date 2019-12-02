## MySQL Database Service 
##
## Purpose: provide the database service 
##
## Author : Simon Li  Oct 2019
##
import mysql.connector
import json

class MySQLService:
    @staticmethod
    def createDatabase(host, dbName):

        # read file
        with open('.mysql.json', 'r') as myConfigFile:
             connData = myConfigFile.read()
        # parse file
        global config 
        config = json.loads(connData)

        mydb = mysql.connector.connect(
            host = config['connection']['host'],
            user = config['connection']['user'],
            passwd = config['connection']['password']
        )
        mycursor = mydb.cursor()

        if MySQLService.existDb(mycursor, dbName):
            pass
        else:
            mycursor.execute("CREATE DATABASE %s" % (dbName))
    
    @staticmethod
    def existDb(cursor, dbName):
        cursor.execute("SHOW DATABASES")
        dbList = []
        for dbTuple in cursor:
            dbList.append(dbTuple[0])

        return dbName in dbList

    def __init__(self, host = 'localhost', dbName = 'mydatabase'):
        MySQLService.createDatabase(host, dbName)  # create database

        global config
        self.__connect = mysql.connector.connect(
                    host = config['connection']['host'],
                    user = config['connection']['user'],
                    passwd = config['connection']['password'],
                    database = dbName         
        )
        
        self.__dbo = dbName
        self.__cursor = self.__connect.cursor() 

    @property
    def dbo(self):
        return self.__dbo 
   
    @property
    def collection(self):
        return self.__connect 
   
    @property
    def table(self):
        return self.__table 
   
    def existTable(self, tableName):
        self.__cursor.execute("SHOW TABLES")

        tabList = []
        for tabTuple in self.__cursor:
            tabList.append(tabTuple[0])
        return tableName in tabList

    @table.setter
    def table(self, tableName):
        self.__table = tableName
        
        if self.existTable(tableName):
            pass
        elif tableName == "tasks":
            self.createTaskTable()

    def createTaskTable(self):
        sql = """CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    done BOOLEAN
                )"""
        
        self.__cursor.execute(sql)

    # List all the records
    def display(self):
        self.__cursor.execute("SELECT * FROM %s" % (self.__table))
        myresult = self.__cursor.fetchall()
        for row in myresult:
            print(row)

    # Return an array of records
    def list(self):
        arrData = []
        self.__cursor.execute("SELECT * FROM %s" % (self.__table))
        myresult = self.__cursor.fetchall()
        for row in myresult:
            arrData.append(row)
        return arrData

    # Spefic to table tasks
    def tasks(self):
        arrData = []
        self.__cursor.execute("SELECT id, title, description, done FROM %s" % (self.__table))
        myresult = self.__cursor.fetchall()
        for row in myresult:
            obj = {"id": row[0], "title": row[1], "description": row[2], "done": row[3]}
            arrData.append(obj)
        return arrData

    # Insert a new record 
    def add(self, tupleVal):
        sql = "INSERT INTO {0} VALUES {1}".format(self.__table, tupleVal) 
        self.__cursor.execute(sql)
        self.__connect.commit()

        print(self.__cursor.rowcount, "record inserted.")

    # Update the existing one
    def update(self, where, dataSet):
        valueSetList = []
        for ea in dataSet:
            if not isinstance(ea["value"], str):
                valueSetList.append(ea["field"] + " = " + str(ea["value"]))
            else:
                valueSetList.append(ea["field"] + " = '" + ea["value"] + "'")

        #print(valueSetList)
        valueSet = ','.join(valueSetList)
        sql = 'UPDATE {0} SET {1} WHERE {2}'.format(self.__table, valueSet, where)
        print("Sql: %s" % sql)
        self.__cursor.execute(sql)

        self.__connect.commit()
        print(self.__cursor.rowcount, "record(s) affected")

    # Remove a record
    def remove(self, where):
        sql = "DELETE FROM {0} WHERE {1}".format(self.__table, where)

        self.__cursor.execute(sql)
        self.__connect.commit()
        print(self.__cursor.rowcount, "record(s) deleted") 

    def clean(self):
        self.__cursor.execute("truncate table {0}".format(self.__table))
        self.__connect.commit()
        
    @classmethod
    def preload(cls, mysql):
        # Test Dataset
        tasks = [
            (
                1,
                u'Buy groceries',
                u'Milk, Cheese, Pizza, Fruit, Tylenol', 
                False
            ),
            (
                2,
                u'Learn Python',
                u'Need to find a good Python tutorial on the web', 
                False
            ),
            (
                3,
                u"Use flask",
                u"Use flask to build RESTful service",
                True
            ) 
        ]   
        for task in tasks:
            mysql.add(task)

    @staticmethod
    def testAdd(mysql):       
        print("** Test Add **")

        newId = mysql.list()[-1][0] + 1 
        #print(newId)      
        task = (newId, "SimonTest", "Test Test", False)
        mysql.add(task)
        mysql.display()
    
    @staticmethod
    def testUpdate(mysql): 
        print("** Test Update **")      
        valueSet = [
            {"field": 'title',       "value": "testUpdate"},
            {"field": 'description', "value": "Test Update Again"},
            {"field": 'done',        "value": True}
        ]
        id = 3
        mysql.update("id = %d" % (id), valueSet)
        mysql.display()

    @staticmethod
    def testRemove(mysql):       
        print("** Test Remove **")   
        mysql.remove("id = %d" % (3))
        mysql.display()

    @staticmethod
    def testList(mysql):
        print("** Test List **")   
        for doc in mysql.list():
            print(doc)

if __name__ == '__main__':  
    mysql = MySQLService()
    mysql.table = "tasks" 

    mysql.clean()
    mysql.preload(mysql)  # class method
    
    print(mysql.tasks( ))
    #MySQLService.testAdd(mysql)  
    #MySQLService.testUpdate(mysql)  # static method
    #MySQLService.testRemove(mysql)  # static method
    #MySQLService.testList(mysql)  # static method