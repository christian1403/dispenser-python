import os
from app.utils.config import Config


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class DatabaseMongo:
    """Configuration for MongoDB connection"""

    MONGODB_URI = Config.DATABASE_URL
    MONGODB_DATABASE = 'dispenser_python' # ngasal aku


    client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

    @staticmethod
    def validate_config():
        """Validate required database configuration"""
        if not DatabaseMongo.MONGODB_URI:
            raise ValueError("MONGODB_URI environment variable is required")
        if not DatabaseMongo.MONGODB_DATABASE:
            raise ValueError("MONGODB_DATABASE environment variable is required")

    
    
    @staticmethod
    def ping():
        """Ping the MongoDB server to check connection"""
        try:
            DatabaseMongo.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")