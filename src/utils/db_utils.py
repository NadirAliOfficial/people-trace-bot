from pymongo import MongoClient


# MongoDB connection setup
def get_mongo_client():
    # Replace this with your MongoDB connection string
    MONGO_URI = "mongodb://localhost:27017"  # For local MongoDB
    # MONGO_URI = "mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority"  # For MongoDB Atlas
    client = MongoClient(MONGO_URI)
    return client


# Get or create a database
def get_database(client, db_name="telegram_bot"):
    return client[db_name]


# Get or create a collection
def get_collection(db, collection_name="users"):
    return db[collection_name]


# Insert or update user data in MongoDB
def save_user_data(collection, user_id, data):
    collection.update_one({"user_id": user_id}, {"$set": data}, upsert=True)


# Retrieve user data from MongoDB
def get_user_data(collection, user_id):
    return collection.find_one({"user_id": user_id})


# Delete user data from MongoDB
def delete_user_data(collection, user_id):
    collection.delete_one({"user_id": user_id})
