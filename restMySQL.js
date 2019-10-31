'use strict';

const express = require('express');
const mysql = require('mysql');

const fs = require('fs');
//const config = JSON.parse(fs.readFileSync('../node/.mysql.json')); 
const config = JSON.parse(fs.readFileSync('.mysql.json')); 

const con = mysql.createConnection({
    host: config.connection.host,
    user: config.connection.user,
    password: config.connection.password,
    database: config.connection.databasee
});

con.connect(err => {
    if (err) throw err;
    console.log("Connected to MySQL");
})

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

// Dummy root request
app.get("/", (req, res) => {
    res.send("Welcome to the rest service of Tasks powered by Nodejs/MySQL.");
})

// List all the tasks (GET)
app.get("/api/v1.0/tasks", (req, res) => {
    const sql = "SELECT * FROM tasks";
    con.query(sql, (err, result, fields) => {
        if (err) 
            res.send(err);
        else {
            //fields.forEach(elem => console.log(elem))
            const tasks = [];
            result.forEach(elem => {
                const task = {
                    "id": elem.id, 
                    "title":  elem.title,
                    "description": elem.description,
                    "done": elem.done
                }
                tasks.push(task);
            })              
            res.send(err? err : tasks);
        }
    });
})

// Get a task per id (GET)
app.get("/api/v1.0/tasks/:id", (req, res) => {
    const sql = `SELECT * FROM tasks WHERE id = ${req.params.id}`; 
    //console.log(sql);  
    con.query(sql, (err, result) => {
        if (err) 
            res.send(err);
        else if (result.length > 0) {
            const task = {
                "id": result[0].id, 
                "title":  result[0].title,
                "description": result[0].description,
                "done": result[0].done
            }
            res.send(task);
        }
        else
            res.send("No task found");    
    });
})

// Insert a task (POST)
app.post("/api/v1.0/tasks", (req, res) => {    
    // a document instance
    //console.log(req.body)
    const sql = `INSERT INTO tasks VALUES(${req.body.id}, '${req.body.title}', '${req.body.description}', ${req.body.done})`;
    con.query(sql, (err, result) => {
        //console.log(result);
        res.send((err)? err : `${result.affectedRows} record inserted: ${result.insertId}`);
    });
})

// Update the task (PUT)
app.put("/api/v1.0/tasks", (req, res) => {
    //console.log(req.body)
    const sql = `UPDATE tasks SET title = '${req.body.title}', description = '${req.body.description}', done = ${req.body.done} WHERE id = ${req.body.id}`;
    con.query(sql, (err, result) => {
       res.send((err)? err : `${result.affectedRows} record(s) updated`);
    });
})

// Delete a task (DELETE)
app.delete("/api/v1.0/tasks", (req, res) => {
    const sql = `DELETE FROM tasks WHERE id = ${req.body.id}`;
    con.query(sql, (err, result) => {
       res.send((err)? err : `Number of records deleted: ${result.affectedRows}`);
    });
})

const port = 8080
app.listen(port, () => {
    console.log(`dbServer app listening on port ${port}.`)
})