const request = require('request');

class oDataSample {
    constructor() {

    }
    
    static printPerson(value) {
        console.log(value['FirstName'] + " " + value['LastName']);
        console.log("User Name: " + value['UserName']);
        const primaryEmail = value['Emails'].length > 0? value['Emails'][0] : "";
        console.log("Email: " + primaryEmail);
    
        if (value['AddressInfo'].length > 0) {
            const address = [value['AddressInfo'][0]['Address'], 
                             value['AddressInfo'][0]['City']['Name'],
                             value['AddressInfo'][0]['City']['Region'],
                             value['AddressInfo'][0]['City']['CountryRegion']].join(', ');
            console.log("Address: " + address);
        }      
        console.log("--------------------------------------------------------------");  
    }

    Query(person = 'russellwhyte', callback) {
        console.log("Test GET");
    
        const url  = !person? 'https://services.odata.org/TripPinRESTierService/People' :
                              `https://services.odata.org/TripPinRESTierService/People('${person}')`;

        request({
            url: `${url}?$format=json`,
            method: 'GET',
            headers:{
                //"Authorization": "Basic <<base64 encoded username:pass>>"",
                "Content-Type": "application/json"
            }  
        }, (err, response, body) => {
            if (err) throw err;
    
            if (typeof callback != 'undefined')
                callback(response, body);
        })   
    }

    Post(callback) {
        console.log("Test POST");
    
        const url = "https://services.odata.org/TripPinRESTierService/People";
        const body = {
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

        request({
            url: url,
            method: 'POST',
            headers:{
                //"Authorization": "Basic <<base64 encoded username:pass>>"",
                "Content-Type": "application/json"
            },
            json: body
        }, (err, response, body) => {
            if (err) throw err;
            console.log("Status: " + response.statusCode);
            //console.log(response);  
            if (typeof callback != 'undefined')
                callback(response, body);   
        })      
    }

    Put(person = 'russellwhyte', callback) {
        console.log("Test PUT");
        const url = `https://services.odata.org/TripPinRESTierService/People('${person}')`;
        console.log(url);
    
        const body = {
            "UserName":"russellwhyte",
            "FirstName":"Russell",
            "LastName":"Whyte",
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

        request({
            url: url,
            method: 'PUT',
            headers:{
                //"Authorization": "Basic <<base64 encoded username:pass>>"",
                "Content-Type": "application/json"
            },
            json: body
        }, (err, response, body) => {
            if (err) throw err;
            console.log("Status: " + response.statusCode);
            //console.log(response);  
            if (typeof callback != 'undefined')
                callback(response, body);   
        })
    }

    Patch(person = 'russellwhyte', callback) {
        console.log("Test PATCH");

        const url = `https://services.odata.org/TripPinRESTierService/People('${person}')`;
        console.log(url);

        const body = {
            "Emails":[
                "testtest@yahoo.com"
            ]
        }

        request({
            url: url,
            method: 'PATCH',
            headers:{
                //"Authorization": "Basic <<base64 encoded username:pass>>"",
                "Content-Type": "application/json"
            },
            json: body
            }, (err, response, body) => {
            if (err) throw err;
            console.log("Status: " + response.statusCode);
            //console.log(response);  
            if (typeof callback != 'undefined')
                callback(response, body);
        })
    }

    Delete(person = 'russellwhyte', callback) {
        console.log("Test DELETE");
        const url = `https://services.odata.org/TripPinRESTierService/People('${person}')`;
        console.log(url);

        request({
                url: url,
                method: 'DELETE',
                headers:{
                //"Authorization": "Basic <<base64 encoded username:pass>>"",
                    "Content-Type": "application/json"
                }
            }, (err, response, body) => {
            if (err) throw err;
            console.log("Status: " + response.statusCode);
            //console.log(response);  
            if (typeof callback != 'undefined')
                callback(response, body);
        })
    }
}

test = new oDataSample();

test.Query(null, (response, body) => {    
//test.Query('russellwhyte', (response, body) => {    
        if (response.statusCode == 200) {
            const obj = JSON.parse(body);
            // console.log(obj);
            if (obj.hasOwnProperty("value")) {
            const people = obj["value"];   
            people.forEach(elem => oDataSample.printPerson(elem));
        }
        else 
            oDataSample.printPerson(obj);
    }
});

//test.Post();
//test.Put();
//test.Patch();
//test.Delete();