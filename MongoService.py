import pymongo

class MongoService:
    def __init__(self, host = 'localhost', port = 27017, dbname = 'mydatabase'):
        '''
        myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        mydb = myclient['mydatabase']
        mycol = mydb["customers"]
        '''
        self.__client = pymongo.MongoClient("mongodb://%s:%d/" % (host, port))
        self.__dbo = self.__client[dbname]
        
    @property
    def dbo(self):
        return self.__dbo 
   
    @dbo.setter
    def dbo(self, dbname):
        self.__dbo = self.__client[dbname]

    @property
    def collection(self):
        return self.__collection 
   
    @collection.setter
    def collection(self, collectionName):
       self.__collection = self.__dbo[collectionName]    

    # Drop the collection
    def drop(self):
        self.__collection.drop()

    # List all the documents
    def display(self, query = {}):
        for doc in self.__collection.find(query, {'_id': False}):
            print(doc)

    # Return an array of documents
    def list(self, query = {}):
        arrDocs = []
        for doc in self.__collection.find(query, {'_id': False}):
            arrDocs.append(doc)
        return arrDocs

    # Insert a new document 
    def add(self, doc):
        result = self.__collection.insert_one(doc.copy())
        return result.inserted_id

    # Update the existing one
    def updateOne(self, query, valueSet):
        newvalues = { "$set": valueSet }
        self.__collection.update_one(query, newvalues)
        
    # Update the existing many
    def update(self, query, valueSet):
        newvalues = { "$set": valueSet }
        x = self.__collection.update_many(query, newvalues)
        return x.modified_count

    # Remove a document
    def removeOne(self, query):
        self.__collection.delete_one(query)

    # Remove all the documents       
    def remove(self, query):    
        x = self.__collection.delete_many(query)
        return x.deleted_count

    def clean(self):
        self.__collection.delete_many({})
    
    @classmethod
    def preload(cls, mongo):
        # Test Dataset
        tasks = [
            {
                'id': 1,
                'title': u'Buy groceries',
                'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
                'done': False
            },
            {
                'id': 2,
                'title': u'Learn Python',
                'description': u'Need to find a good Python tutorial on the web', 
                'done': False
            },
            {
                "id": 3,
                "title": u"Use flask",
                "description": u"Use flask to build RESTful service",
                "done": True
            } 
        ]   
        for task in tasks:
            mongo.add(task)

    @staticmethod
    def testAdd(mongo):       
        print("** Test Add **")   
        task = {
            'id': mongo.list()[-1]['id'] + 1,
            'title': "SimonTest",
            'description': "Test Test",
            'done': False
        }
        mongo.add(task)
        mongo.display()
    
    @staticmethod
    def testUpdate(mongo): 
        print("** Test Update **")      
        valueSet = {
            'title': "testUpdate",
            'description': "Test Update",
            'done': True
        }
        mongo.updateOne({"id": 4}, valueSet)
        mongo.display()

    @staticmethod
    def testRemove(mongo):       
        print("** Test Remove **")   
        mongo.removeOne({"id": 4})
        mongo.display()

    @staticmethod
    def testList(mongo):
        print("** Test List **")   
        for doc in mongo.list():
            print(doc)

if __name__ == '__main__':  
    mongo = MongoService()
    mongo.collection = "tasks"  

    #mongo.drop()
    mongo.clean()
    mongo.preload(mongo)   # class method
    #mongo.display()
    
    MongoService.testAdd(mongo)  # static method
    MongoService.testUpdate(mongo)  # static method
    MongoService.testRemove(mongo)  # static method
    MongoService.testList(mongo)  # static method