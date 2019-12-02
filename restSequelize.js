// Node/Sequelize Service for tasks 
//
// Sequelize is a promise-based Node.js ORM for Postgres, MySQL, MariaDB, 
// SQLite and Microsoft SQL Server.
//
// Purpose: provide restful web api for tasks 
//
// Author : Simon Li  Dec 2019
//
//  Prerequisite: a database driver module (mysql2)
'use strict';

// Load the enviroment variables to process from .env
require('dotenv').config()
const databaseUrl = process.env.DATABASEURL;

const Sequelize = require('sequelize');
const {DataTypes: DataType} = require('sequelize');

const sequelize = new Sequelize(databaseUrl, {
    define: {
      freezeTableName: true
    },
    logging: console.log
});

const Task = sequelize.define('tasks', {
    id: {
           type: DataType.INTEGER,
           allowNull: false,
           primaryKey: true,
           autoIncrement: true
    }, 
	
	title: {
        type: DataType.STRING,
        allowNull: false,
	},

	description: {
        type: DataType.STRING,
	},

	done: {
        type: DataType.BOOLEAN,
        defaultValue: false
    }
});

const tasks = [
    {
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': false
    },
    {
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web', 
        'done': false
    },
    {
        "title": "Use flask",
        "description": "Use flask to build RESTful service",
        "done": true
    },
    {
        "title": "Learn OData",
        "description": "Learn OData to build Restful APIU",
        "done": false
    } 
];

const bRefreshed = false;

// Create the tables:
if (!bRefreshed)
    Task.sync().then( () => {
        console.log("The tasks table has been created");
    }).catch(error => {
        throw new Error("oooh, did you enter wrong database credentials?");
    });
else
    Task.sync({force: true}).then(() => { // this will drop the table first and re-create it afterwards
        tasks.forEach(elem => {
            Task.create(elem).then(task => console.log(`Task ${task.title} was inserted`))
        })
    }).catch(error => {
        throw new Error("oooh, did you enter wrong database credentials?");
    });

const express = require('express');
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
    res.send("Welcome to the rest service of Tasks powered by Sequelize.");
})

// List all the tasks (GET)
app.get("/api/v1.0/tasks", (req, res) => {
    Task.findAll().then(result => {
        //console.log(result);
        const tasks = [];
        result.forEach(elem => {
            //const task = {
            //    "id": elem.dataValues.id, 
            //    "title":  elem.dataValues.title,
            //    "description": elem.dataValues.description,
            //    "done": elem.dataValues.done
            //}
            //tasks.push(task);
            tasks.push(elem.dataValues);
        })              
        res.send(tasks);
    });
})

// Get a task per id (GET)
app.get("/api/v1.0/tasks/:id", (req, res) => {
    Task.findOne({ where: { id: req.params.id } }).then(task => {
        res.send(task);
    });
})

// Insert a task (POST)
app.post("/api/v1.0/tasks", (req, res) => {    
    // a document instance
    //console.log(req.body)
    const task = req.body; 
    Task.create(task).then(restask =>{
        res.send(`Task ${restask.title} was inserted`);
    })
})

// Update the task (PUT)
app.put("/api/v1.0/tasks", (req, res) => {
    //console.log(req.body)
    Task.update({
            title: req.body.title,
            description: req.body.description, 
            done: req.body.done
        },
        { where: { id: req.body.id }}
    ).then(result => {
        res.send(`${result} record(s) updated - ${req.body.id}`);
    })
})

// Update the task (PATCH)
app.patch("/api/v1.0/tasks", (req, res) => {
    //console.log(req.body)
    const task = {...req.body};
    delete task["id"];
    
    Task.update(task, {where: {id: req.body.id}}
    ).then(result => {
        res.send(`${result} record(s) patched - ${req.body.id}`);
    })
})

// Delete a task (DELETE)
app.delete("/api/v1.0/tasks", (req, res) => {
    Task.destroy({where: {id: req.body.id}}).then(result => {
       res.send(`Number of records deleted: ${result}`);
    });
})

const port = 8080
app.listen(port, () => {
    console.log(`dbServer app listening on port ${port}.`)
})