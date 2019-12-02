## Python sample restful api service(CRUD) to consume an OData
## https://services.odata.org/TripPinRESTierService/People
##
## Purpose: provide restful api to consume an OData service 
##
## Author : Simon Li  Nov 2019
##
import requests

class oDataSample:
    def __init__(self, url = 'https://services.odata.org/TripPinRESTierService/People'):
        self.url = url

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
    def get(self, person = "russellwhyte"):
        print("Test GET")
    
        #url  = 'https://services.odata.org/TripPinRESTierService/People?$format=json'
        if person.upper() == "ALL":
            url = self.url
        else:
            url =  "%s('%s')" % (self.url, person)

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
    def post(self):
        print("Test POST")

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

        response = requests.post(self.url, json = body)
        #print(response)
        print("status: %d" % response.status_code)

        # Get the 
        #json = response.json()
        #print(json)

    # Update/replace - PUT
    def put(self, person = 'russellwhyte'):
        print("Test PUT")
    
        url = "%s('%s')" % (self.url, person)
    
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
        #print(response)
        print("status: %d" % response.status_code)
        # Get the 
        #json = response.json()
        #print(json)

    # Update/portion - PATCH
    def patch(self, person = 'russellwhyte'):  
        print("Test PATCH")
      
        url = "%s('%s')" % (self.url, person)
        #print(url)
        body = {
            "FirstName": "Mirs",
            "LastName": "King"
        }
        response = requests.patch(url, json = body)
        #print(response)
        print("status: %d" % response.status_code)
        # Get the 
        #json = response.json()
        #print(json)

    # Delete - DELETE
    def delete(self, person = 'russellwhyte'):    
        print("Test DELETE")
    
        url = "%s('%s')" % (self.url, person)
        #print(url)
        response = requests.delete(url)
        #print(response)
        print("status: %d" % response.status_code)
        # Get the 
        #json = response.json()
        #print(json)

odata = oDataSample()

odata.get("ALL")       
#odata.get()       

#url = "%s('%s')" % (odata.url, 'peter'); print(url)

#odata.post()
#odata.put()
#odata.patch()
#odata.delete()