from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import Config
import streamlit as st

@st.cache_resource
def connect_to_db():
    """Connect to db."""
    # establish db connection
    client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'))

    # ping
    try:
        client.admin.command('ping')
        print("Connected to db.")
    except Exception as e:
        print(e)

    # connect to db
    db = client["aus_prop"]
    return db

def add_to_collection(db, collection_name, df):
    """Add data to collection."""
    collection = db[collection_name]
    collection.insert_many(df.to_dict("index").values())

def get_collection_names():
    """Get list of collections in the database"""
    db = st.session_state.db
    if not db:
        return []
        
    return db.list_collection_names()