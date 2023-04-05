from pymongo import MongoClient

MONGO_HOST = "mongodb://localhost"
MONGO_PORT = 27017
MONGO_DB = "sanic"

db = None

async def get_database():
    global db

    # If the database connection has already been established, return it
    if db is not None:
        return db

    try:
        # Create a new database connection
        client = MongoClient("mongodb://localhost:27017/")
        db = client["sanic"]
    except Exception as e:
        # Handle any errors that occur when establishing the connection
        print(f"Failed to establish database connection: {e}")
        db = None

    return db
