// Node/MongoDb Service for tasks 
//
// Purpose: provide restful web api for tasks 
//
// Author : Simon Li  Nov 2019
//
'use strict';

const express = require('express');
const goose = require("mongoose");

const db = goose.connect(`mongodb://localhost:27017/mydatabase`, 
    {useNewUrlParser: true, useUnifiedTopology: true}, (err, response) => {
    if (err) 
       console.log(err);  
    else 
       console.log('Connected to ' + db, ' + ', response); 
});

//const dbo = goose.connection; 
//dbo.on('error', console.error.bind(console, 'connection error:')); 
//dbo.once('open', () => {
//    console.log("Connection Successful!");
//});

const app = express()

app.use(function(req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});

// Parse URL-encoded bodies (as sent by HTML forms)
//app.use(express.urlencoded());  -- no needed

// Parse JSON bodies (as sent by API clients)
app.use(express.json());

const TasksSchema = new goose.Schema({
    id: { type: Number, required: true },
    title: { type: String },
    description: { type: String },
    done: { type: Boolean, default: false}
});

//const mongoosePaginate = require('mongoose-paginate');
//TasksSchema.plugin(mongoosePaginate);

// compile schema to model
const TaskModel = goose.model('Tasks', TasksSchema);

// Dummy root request
app.get("/", (req, res) => {
    res.send({data: "Welcome to the rest service of Tasks powered by Nodejs/MongoDb."});
})

// List all the tasks (GET)
app.get("/api/v1.0/tasks", (req, res) => {
    TaskModel.find({}, {_id: 0}, (err, data) => {
        res.send(err? err : data);
    });
})

// Get a task per id (GET)
app.get("/api/v1.0/tasks/:id", (req, res) => {
    TaskModel.find({ id: req.params.id }, {_id: 0}, (err, data) => {
        res.send(err? err : data);
    });
})

// Insert a task (POST)
app.post("/api/v1.0/tasks", (req, res) => {    
    // a document instance
    console.log(req.body)
    const task1 = new TaskModel(req.body)
    task1.save((err, data) => { 
        res.send(err? err : {data: "Record has been inserted..!!"});
    });
})

// Update the task (PUT)
app.put("/api/v1.0/tasks", (req, res) => {
    console.log(req.body)
    TaskModel.updateOne({ id: req.body.id }, { "$set": req.body},
            err => {
                res.send(err? err : {data: "Record has been updated..!!"});
            });
})

// Delete a task (DELETE)
app.delete("/api/v1.0/tasks", (req, res) => {
    //console.log("ID to be deleted: " + req.body.id)
    TaskModel.deleteOne({ id: req.body.id }, err => {
        res.send(err? err : { data: "Record has been Deleted..!!" });
    });
})

const port = 8080
app.listen(port, () => {
    console.log(`dbServer app listening on port ${port}.`)
})