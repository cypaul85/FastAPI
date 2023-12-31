from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel

class Todo(BaseModel):
    title: str
    description: str

app = FastAPI()

origins = [
    "https://localhost:3000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# MongoDB Connection details
mongo_host = "localhost"
mongo_port = 27017
mongo_db = "testDB"
mongo_collection = "todo"

# Connect to the MongoDB server
client = MongoClient(mongo_host, mongo_port)
db = client[mongo_db]
collection = db[mongo_collection]

@app.get("/")
def home():
    return {"Message":"Hello World!"}

@app.get("/todos")
def read_todos():
    todos = list(collection.find({}, {"_id": 0}))
    return {"data": todos}

@app.get("/todos/{title}")
def read_todo_by_title(title: str):
    todo = collection.find_one({"title": title}, {"_id":0})
    if not todo:
        return {"Message": "Todo not found"}
    return {"data": todo}

@app.post("todos")
def create_todo(todo: Todo):
    result = collection.insert_one(todo.dict())
    return{
        "id":str(result.inserted_id),
        "title":todo.title,
        "description":todo.description
    }

@app.delete("/todos")
def delete_todo_by_title(title:str):
    result = collection.delete_one({"title":title})
    if result.deleted_count == 0:
        return {"Message": "Todo not found"}
    return {"Message": "Todo deleted successfully"}
