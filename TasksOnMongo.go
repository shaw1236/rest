// https://tutorialedge.net/golang/creating-restful-api-with-golang/

package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
	"strings"

	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
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
	fmt.Println("Endpoint Hit: returnSingleTask")
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
	//fmt.Println("Key: ", key)
	for _, task := range Tasks {
		if task.Id == key {
			json.NewEncoder(w).Encode(task)
			return
		}
	}

	message := fmt.Sprintf("{\"status\": %d, \"message\": \"Not found task id: %d\"}", 404, key)
	fmt.Fprintf(w, message)
}

// Method: GET
func returnDbSingleTask(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Endpoint Hit: returnDbSingleTask")
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

	task, err := dbFind(key)
	if err == nil {
		json.NewEncoder(w).Encode(task)
		return
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

	//myRouter.HandleFunc("/task/{id}", returnSingleTask)
	myRouter.HandleFunc("/task/{id}", returnDbSingleTask)

	myRouter.HandleFunc("/task", createNewTask).Methods("POST")

	myRouter.HandleFunc("/task/{id}", deleteTask).Methods("DELETE")

	myRouter.HandleFunc("/task/{id}", updateTask).Methods("PUT")

	// finally, instead of passing in nil, we want
	// to pass in our newly created router as the second
	// argument
	log.Fatal(http.ListenAndServe(":10000", myRouter))
}

func dbConnect() (*mongo.Client, *mongo.Collection) {
	// Set client options
	clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")

	// Connect to MongoDB
	client, err := mongo.Connect(context.TODO(), clientOptions)

	if err != nil {
		log.Fatal(err)
	}

	// Check the connection
	err = client.Ping(context.TODO(), nil)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Connected to MongoDB!")

	dbo := client.Database("mydatabase")
	collection := dbo.Collection("tasks")

	return client, collection
}

func dbClose(client *mongo.Client) {
	err := client.Disconnect(context.TODO())

	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Connection to MongoDB closed.")
}

func getTasksFromDatabase() {
	// Open up our database connection.
	client, collection := dbConnect()

	// defer the close till after the main function has finished executing
	defer dbClose(client)

	// Execute the query
	// Passing bson.D{{}} as the filter matches all documents in the collection
	// Pass these options to the Find method
	findOptions := options.Find()
	cur, err := collection.Find(context.TODO(), bson.D{{}}, findOptions)
	if err != nil {
		log.Fatal(err)
	}

	// Iterating through the cursor allows us to decode documents one at a time
	for cur.Next(context.TODO()) {
		// create a value into which the single document can be decoded
		var elem Task
		err := cur.Decode(&elem)
		if err != nil {
			log.Fatal(err)
		}

		Tasks = append(Tasks, elem)
	}

	if err := cur.Err(); err != nil {
		log.Fatal(err)
	}

	// Close the cursor once finished
	cur.Close(context.TODO())

	fmt.Printf("Found multiple documents (array of pointers): %+v\n", Tasks)
}

func dbFind(id int) (Task, error) {
	// Open up our database connection.
	client, collection := dbConnect()

	// defer the close till after the function has finished executing
	defer dbClose(client)

	filter := bson.D{{"id", id}}
	//fmt.Println("filer", filter)
	// create a value into which the result can be decoded
	var task Task

	err := collection.FindOne(context.TODO(), filter).Decode(&task)
	//fmt.Printf("Found a single document: %+v\n", task)

	return task, err
}

func dbInsert(task Task) {
	// Open up our database connection.
	client, collection := dbConnect()

	// defer the close till after the function has finished executing
	defer dbClose(client)

	//timestamp := time.Now().Format("2006-01-02 15:04:05")
	//fmt.Println("Timestamp: ", timestamp)

	task.Id = len(Tasks) + 1
	task.Done = false

	insertResult, err := collection.InsertOne(context.TODO(), task)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Inserted a single document: ", insertResult.InsertedID)
}

func dbUpdate(task Task) {
	// Open up our database connection.
	client, collection := dbConnect()

	// defer the close till after the function has finished executing
	defer dbClose(client)

	filter := bson.D{{"id", task.Id}}

	update := bson.D{
		{"$set", bson.D{
			{"title", task.Title}, {"description", task.Description}, {"done", task.Done},
		},
		},
	}

	updateResult, err := collection.UpdateOne(context.TODO(), filter, update)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Matched %v documents and updated %v documents.\n", updateResult.MatchedCount,
		updateResult.ModifiedCount)
}

func dbDelete(id int) {
	// Open up our database connection.
	client, collection := dbConnect()

	// defer the close till after the function has finished executing
	defer dbClose(client)

	filter := bson.D{{"id", id}}

	deleteResult, err := collection.DeleteOne(context.TODO(), filter)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Deleted %v documents in the tasks collection\n", deleteResult.DeletedCount)
}

func main() {
	fmt.Println("Rest API - Mongo")
	fmt.Println(bson.D{
		{"id", 100}, {"title", "Title"}, {"description", "Description"}, {"done", false},
	})
	fmt.Println()

	go getTasksFromDatabase()
	//fmt.Println(Tasks)

	fmt.Println("Server start at port: ", 10000)
	handleRequests()
}
