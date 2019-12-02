// Node sample restful api service(CRUD) to consume an OData
// https://services.odata.org/TripPinRESTierService/People
//
// Purpose: provide restful api to consume an OData service 
//
// Author : Simon Li  Nov 2019
//
// https://help.sap.com/saphelp_mii150sp04/helpdata/EN/54/5aff512ec09b33e10000000a44538d/content.htm?no_cache=true
const request = require('request');

class oDataSample {
    constructor(key = '(S(i4oopvr0nc4j1ta5ytvp5gtz))', 
                url = 'https://services.odata.org/TripPinRESTierService', 
                EntitySet = 'People') {  
        this.url = `${url}/${key}/${EntitySet}`;
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

    static output(response) {
        if (response.statusCode == 200 || 
            response.statusCode == 201) {
            let obj = {};
            if (typeof response.body == 'object')
                obj = response.body;
            else
                obj = JSON.parse(response.body);
    
            // console.log(obj);
            if (obj.hasOwnProperty("value")) {
                const people = obj["value"];   
                people.forEach(elem => oDataSample.printPerson(elem));
            }
            else 
                oDataSample.printPerson(obj);
        }
    }

    static mylog(response) {
        console.log("**** Response ****");
        console.log(response);
    }
    
    // Read - GET
    get(person = 'russellwhyte', callback) {
        console.log("Test GET");
    
        const url  = !person? this.url : `${this.url}('${person}')`;

        request({
            //url: `${url}?$format=json`,
            url: url,
            method: 'GET',
            headers:{
                //"Authorization": "Basic <<base64 encoded username:pass>>"",
                "Content-Type": "application/json"
            }  
        }, (err, response, body) => {
            if (err) throw err;
    
            if (typeof callback != 'undefined')
                callback(response);
        })   
    }

    // Create - POST
    post(callback) {
        console.log("Test POST");
    
        const body = {
            "UserName":"simon",
            "FirstName":"Simon",
            "LastName":"Test",
            "Emails":[
                "testtest@example.com"
            ],
            "AddressInfo": [
                {
                    "Address": "1000 Suffolk Ln.",
                    "City": {
                        "Name": "Boise",
                        "CountryRegion": "United States",
                        "Region": "ID"
                    }
                }
            ]
        }

        request({
            url: this.url,
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
                callback(response);   
        })      
    }

    // Update/replace - PUT
    put(person = 'russellwhyte', callback) {
        console.log("Test PUT");
        const url = `${this.url}('${person}')`;
        console.log(url);
    
        const body = {
            "UserName":"simon",
            "FirstName":"Simon",
            "LastName":"Simon",
            "Emails":[
                "testtest2@example.com"
            ],
            "AddressInfo": [
                {
                    "Address": "2000 Suffolk Ln.",
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
                callback(response);   
        })
    }

    // Update/portion - PATCH
    patch(person = 'russellwhyte', callback) {
        console.log("Test PATCH");

        const url = `${this.url}('${person}')`;
        //console.log(url);

        const body = {
            "Emails":[
                "testtest@gmail.com"
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
                callback(response);
        })
    }

    // Delete - DELETE
    delete(person = 'russellwhyte', callback) {
        console.log("Test DELETE");
        const url = `${this.url}('${person}')`;
        //console.log(url);

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
                callback(response);
        })
    }
}

odata = new oDataSample();

odata.get(null, response => oDataSample.output(response));     
//odata.get('russellwhyte', response => oDataSample.output(response));    
//odata.get('simon', response => oDataSample.output(response));

//odata.post(response => oDataSample.output(response));

//odata.put('simon', response => oDataSample.output(response));
//odata.patch('russellwhyte', response => oDataSample.output(response));
//odata.delete('simon', response => oDataSample.output(response));