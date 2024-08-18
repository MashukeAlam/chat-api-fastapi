from pymongo import MongoClient
from pymongo.collection import Collection


# Replace '62.72.7.168' with the IP of your MongoDB server
mongo_host = "62.72.7.168"
mongo_port = 27017

# Connect to the MongoDB server
client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}")

db = client["chat_db"]

# Collections
users_collection: Collection = db["users"]
messages_collection: Collection = db["messages"]