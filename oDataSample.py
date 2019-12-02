## Python sample restful api service(CRUD) to consume an OData
## https://services.odata.org/TripPinRESTierService/People
##
## Purpose: provide restful api to consume an OData service 
##
## Author : Simon Li  Nov 2019
##
import requests

class oDataSample:
    def __init__(self):
        pass

    @staticmethod
    def printPerson(value):
        if 'FirstName' in value.keys():
            print(value['FirstName'] + " " + value['LastName'] )
        print("User Name: " + value['UserName'] if 'FirstName' in value.keys() else '')
        if 'Emails' in value.keys() and len(value['Emails']) > 0:
            print("Email: " + value['Emails'][0]) 
        if 'AddressInfo' in value.keys() and len(value['AddressInfo']) > 0:
            address = ', '.join([value['AddressInfo'][0]['Address'], 
                            value['AddressInfo'][0]['City']['Name'],
                            value['AddressInfo'][0]['City']['Region'],
                            value['AddressInfo'][0]['City']['CountryRegion']])
            print("Address: " + address)  
        print("--------------------------------------------------------------")  

    # Read - GET
    def Query(self, person = "russellwhyte"):
        print("Test GET")
    
        #url  = 'https://services.odata.org/TripPinRESTierService/People?$format=json'
        if person.upper() == "ALL":
            url = 'https://services.odata.org/TripPinRESTierService/People'
        else:
            url =  "https://services.odata.org/TripPinRESTierService/People('%s')" % (person)

        # Get the response - <Response [200]>
        response = requests.get(url)
        #print(response)

        # Get the 
        json = response.json()
        #print(json)

        if 'value' in json.keys():
            for value in json['value']:
                oDataSample.printPerson(value)
        else:
            oDataSample.printPerson(json)

    # Create - POST
    def Post(self):
        print("Test POST")

        url = 'https://services.odata.org/TripPinRESTierService/People'
        body = {
            "UserName":"simon",
            "FirstName":"Simon",
            "LastName":"Test",
            "Emails":[
                "testtest@example.com"
            ],
            "AddressInfo": [
                {
                    "Address": "187 Suffolk Ln.",
                    "City": {
                        "Name": "Boise",
                        "CountryRegion": "United States",
                        "Region": "ID"
                    }
                }
            ]
        }

        response = requests.post(url, json = body)
        print(response)
        # Get the 
        json = response.json()
        print(json)

    # Update/replace - PUT
    def Put(self, person = 'russellwhyte'):
        print("Test PUT")
    
        url = "https://services.odata.org/TripPinRESTierService/People('%s')" % person
    
        body = {
            "UserName":"russellwhyte",
            "FirstName":"Russell",
            "LastName":"Whyte",
            "Emails":[
                "testtest1@example.com",
                "testtest2@example.com",
                "Russell@example.com"
            ],
            "AddressInfo": [
                {
                    "Address": "187 Suffolk Ln.",
                    "City": {
                        "Name": "Boise",
                        "CountryRegion": "United States",
                        "Region": "ID"
                    }
                }
            ]
        }

        response = requests.put(url, json = body)
        print(response)
        # Get the 
        json = response.json()
        print(json)

    # Update/portion - PATCH
    def Patch(self, person = 'russellwhyte'):  
        print("Test PATCH")
      
        url = "https://services.odata.org/TripPinRESTierService/People('%s')" % person
        #print(url)
        body = {
            "FirstName": "Mirs",
            "LastName": "King"
        }
        response = requests.patch(url, json = body)
        print(response)
        # Get the 
        json = response.json()
        print(json)

    # Delete - DELETE
    def Delete(self, person = 'russellwhyte'):    
        print("Test DELETE")
    
        url = "https://services.odata.org/TripPinRESTierService/People('%s')" % person
        #print(url)
        response = requests.delete(url)
        print(response)
        # Get the 
        json = response.json()
        print(json)

test = oDataSample()
test.Query("ALL")       
#test.Post()
#test.Put()
#test.Patch()
#test.Delete()