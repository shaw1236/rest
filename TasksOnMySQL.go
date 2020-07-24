// https://tutorialedge.net/golang/creating-restful-api-with-golang/
package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
	"strings"
	"time"

	_ "github.com/go-sql-driver/mysql"
	"github.com/gorilla/mux"
)

// Must start with a upper case character
type Task struct {
	Id          int    `json:"id"`
	Title       string `json:"title"`
	Description string `json:"description"`
	Done        bool   `json:"done"`
}

// to simulate a database
var Tasks []Task

// Method: PUT (PATCH?. MERGE)
func updateTask(w http.ResponseWriter, r *http.Request) {
	reqBody, _ := ioutil.ReadAll(r.Body)

	//fmt.Fprintf(w, "%+v", string(reqBody))  // check the data
	var myTask Task
	json.Unmarshal(reqBody, &myTask)

	// update our global task
	for index, task := range Tasks {
		// if our id path parameter matches one of our
		// articles
		if task.Id == myTask.Id {
			// updates our Tasks array
			var message string
			if task == myTask {
				message = fmt.Sprintf("{\"status\": %d,\"message\": \"task %d has not been changed\"}", 200, myTask.Id)
			} else {
				Tasks[index] = myTask
				go dbUpdate(myTask)
				message = fmt.Sprintf("{\"status\": %d,\"message\": \"task %d has been update\"}", 200, myTask.Id)
			}

			fmt.Fprintf(w, message)
			break // dummy code
		}
	}
}

// Method: DELETE
func deleteTask(w http.ResponseWriter, r *http.Request) {
	// once again, we will need to parse the path parameters
	vars := mux.Vars(r)
	// we will need to extract the `id` of the article we
	// wish to delete
	id, err := strconv.Atoi(vars["id"])
	if err != nil {
		error := strings.ReplaceAll(err.Error(), "\"", "'")
		message := fmt.Sprintf("{\"status\": %d,\"message\": \"%s\"}", 409, error)
		fmt.Fprintf(w, message)
		//fmt.Println(message)
		return
	}

	// we then need to loop through all our articles
	for index, task := range Tasks {
		// if our id path parameter matches one of our
		// articles
		if task.Id == id {
			// updates our Tasks array to remove the
			// task
			Tasks = append(Tasks[:index], Tasks[index+1:]...)
			go dbDelete(id)
			message := fmt.Sprintf("{\"status\": %d,\"message\": \"task %d has been removed\"}", 200, id)
			fmt.Fprintf(w, message)
			break // dummy code
		}
	}
}

// Method: POST
func createNewTask(w http.ResponseWriter, r *http.Request) {
	// get the body of our POST request
	// return the string response containing the request body
	reqBody, _ := ioutil.ReadAll(r.Body)

	//fmt.Fprintf(w, "%+v", string(reqBody))  // check the data
	var task Task
	json.Unmarshal(reqBody, &task)
	// update our global task array to include
	// our new task
	Tasks = append(Tasks, task)

	go dbInsert(task)

	json.NewEncoder(w).Encode(task)
}

// Method: GET
func returnSingleTask(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	//key := strconv.Atoi(vars["id"])
	key, err := strconv.Atoi(vars["id"])
	if err != nil {
		error := strings.ReplaceAll(err.Error(), "\"", "'")
		message := fmt.Sprintf("{\"status\": %d,\"message\": \"%s\"}", 409, error)
		fmt.Fprintf(w, message)
		//fmt.Println(message)
		return
	}

	//fmt.Fprintf(w, "Key: " + key)
	for _, task := range Tasks {
		if task.Id == key {
			json.NewEncoder(w).Encode(task)
			return
		}
	}

	message := fmt.Sprintf("{\"status\": %d, \"message\": \"Not found task id: %d\"}", 404, key)
	fmt.Fprintf(w, message)
}

// Method: GET (Query)
func returnAllTasks(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Endpoint Hit: returnAllTasks")
	//fmt.Println(Tasks);
	json.NewEncoder(w).Encode(Tasks)
}

func homePage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Welcome to the Home Page!")
	fmt.Println("Endpoint Hit: homePage")
}

// Existing code from above
func handleRequests() {
	// creates a new instance of a mux router
	myRouter := mux.NewRouter().StrictSlash(true)

	// replace http.HandleFunc with myRouter.HandleFunc
	myRouter.HandleFunc("/", homePage)

	myRouter.HandleFunc("/all", returnAllTasks)
	myRouter.HandleFunc("/tasks", returnAllTasks)

	myRouter.HandleFunc("/task/{id}", returnSingleTask)

	myRouter.HandleFunc("/task", createNewTask).Methods("POST")

	myRouter.HandleFunc("/task/{id}", deleteTask).Methods("DELETE")

	myRouter.HandleFunc("/task/{id}", updateTask).Methods("PUT")

	// finally, instead of passing in nil, we want
	// to pass in our newly created router as the second
	// argument
	log.Fatal(http.ListenAndServe(":10000", myRouter))
}

func getTasksFromDatabase() {
	// Open up our database connection.
	db := dbOpen()

	// defer the close till after the main function has finished executing
	defer db.Close()

	// Execute the query
	results, err := db.Query("SELECT Id, Title, Description, Done FROM tasks")
	if err != nil {
		panic(err.Error()) // proper error handling instead of panic in your app
	}
	for results.Next() {
		var task Task
		// for each row, scan the result into our tag composite object
		err = results.Scan(&task.Id, &task.Title, &task.Description, &task.Done)
		if err != nil {
			panic(err.Error()) // proper error handling instead of panic in your app
		}

		//Tasks = append(Tasks, Task{task.id, task.title, task.description, task.done})
		Tasks = append(Tasks, task)
	}
}

func dbOpen() *sql.DB {
	// Open up our database connection.
	// DATABASEURL=mysql://root:Shaw1236$@localhost/mydb
	db, err := sql.Open("mysql", "root:Shaw1236$@tcp(localhost:3306)/mydb")

	// if there is an error opening the connection, handle it
	if err != nil {
		panic(err.Error())
	}
	return db
}

func dbInsert(task Task) {
	db := dbOpen()

	// defer the close till after the main function has finished
	defer db.Close()

	// Execute the query
	timestamp := time.Now().Format("2006-01-02 15:04:05")
	fmt.Println("Timestamp: ", timestamp)

	// perform a db.Query insert
	sql := fmt.Sprintf("INSERT INTO tasks(title, descriptiohn, done, createdAt, updatedAt) VALUES('%s', '%s', %t, '%s', '%s'",
		task.Title, task.Description, task.Done, timestamp, timestamp)
	fmt.Println("sql: ", sql)

	_, err := db.Query(sql)
	if err != nil {
		panic(err.Error()) // proper error handling instead of panic in your app
	}
}

func dbUpdate(task Task) {
	db := dbOpen()

	// defer the close till after the main function has finished
	defer db.Close()

	// Execute the query
	timestamp := time.Now().Format("2006-01-02 15:04:05")
	fmt.Println("Timestamp: ", timestamp)

	// perform a db.Query insert
	sql := fmt.Sprintf("UPDATE tasks set title = '%s' description = '%s' done = %t, updatedAt = '%s'",
		task.Title, task.Description, task.Done, timestamp)
	fmt.Println("sql: ", sql)

	_, err := db.Query(sql)
	if err != nil {
		panic(err.Error()) // proper error handling instead of panic in your app
	}
}

func dbDelete(id int) {
	db := dbOpen()

	// defer the close till after the main function has finished
	defer db.Close()

	// perform a db.delete
	sql := fmt.Sprintf("DELETE FROM tasks WHERE id = %d", id)
	fmt.Println("sql: ", sql)

	_, err := db.Query(sql)
	if err != nil {
		panic(err.Error()) // proper error handling instead of panic in your app
	}
}

func main() {
	fmt.Println("Rest API v2.0 - Mux Routers")

	go getTasksFromDatabase()
	//fmt.Println(Tasks)

	fmt.Println("Server start at port: ", 10000)
	handleRequests()
}
