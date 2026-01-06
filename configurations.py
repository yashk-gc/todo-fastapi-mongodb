from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://yashk_gc:Y%40shGC070904@crud.tyfbwnk.mongodb.net/?appName=CRUD"

client = MongoClient(uri, server_api=ServerApi("1"))

db = client.todo_db
collection = db["todo_data"]


