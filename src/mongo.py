import os
from dotenv import load_dotenv
from pymongo import MongoClient
import polars as pl
import pandas as pd
import pymongo

load_dotenv()
# MongoDB connection parameters
mongo_host = os.getenv("MONGODB_HOST")
mongo_port = 27017
mongo_user = os.getenv("MONGODB_USER")
mongo_pass = os.getenv("MONGODB_PASSWORD")
mongo_auth_source = 'admin' 

if not mongo_port:
    raise ValueError("MONGODB_PORT not set")
if not mongo_user:
    raise ValueError("MONGODB_USER not set")
if not mongo_pass:
    raise ValueError("MONGODB_PASSWORD not set")


client = pymongo.MongoClient(host=mongo_host,
                             port=mongo_port,
                             username=mongo_user,
                             password=mongo_pass,
                             authSource=mongo_auth_source)

# Check if MongoDB is reachable and authenticate
try:
    # List all databases in MongoDB
    databases = client.list_database_names()
    print("MongoDB connection successful. Databases available:", databases)
except pymongo.errors.ConnectionFailure:
    print("Failed to connect to MongoDB.")


def get_collection(layer: str, database: str) -> MongoClient:
    """
    Retrieves a collection from the specified layer and database in MongoDB.

    Args:
        layer (str): The name of the layer in MongoDB.
        database (str): The name of the database in MongoDB.

    Returns:
        pymongo.collection.Collection: The collection object.

    """
    client = pymongo.MongoClient(host=mongo_host,
                             port=mongo_port,
                             username=mongo_user,
                             password=mongo_pass,
                             authSource=mongo_auth_source)
    db = client[layer]
    collection = db[database]
    return collection

def insert_document(collection: MongoClient, document: list[dict]) -> None:
    """
    Inserts a list of documents into a MongoDB collection.

    Args:
        collection (MongoClient): The MongoDB collection to insert the documents into.
        document (list[dict]): The list of documents to be inserted.

    Returns:
        None
    """
    for doc in document:
        if '_id' in doc:
            # Update the existing document or insert a new document if no matching document is found
            collection.update_one({'_id': doc['_id']}, {'$set': doc}, upsert=True)
        else:
            # Insert a new document
            collection.insert_one(doc)

def store_data(layer: str, database: str, document: list[dict]) -> None:
    """
    Stores the given document in the specified layer and database.

    Args:
        layer (str): The layer where the document will be stored.
        database (str): The database where the document will be stored.
        document (list[dict]): The document to be stored.

    Returns:
        None
    """
    collection = get_collection(layer, database)
    insert_document(collection, document)

def get_all_data(layer: str, database: str) -> list[dict]:
    """
    Retrieve all data from a specific layer in a given database.

    Args:
        layer (str): The name of the layer to retrieve data from.
        database (str): The name of the database to retrieve data from.

    Returns:
        list[dict]: A list of dictionaries containing the retrieved data.
    """
    collection = get_collection(layer, database)
    return collection.find()

def get_dataframe_from_mongoDB(layer: str, database: str) -> pd.DataFrame:
    """
    Retrieves data from MongoDB for a given layer and database, and returns it as a pandas DataFrame.

    Parameters:
    layer (str): The layer to retrieve data from.
    database (str): The database to retrieve data from.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the retrieved data.
    """
    data = get_all_data(layer, database)
    return pd.DataFrame(data)
