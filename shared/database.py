import os
import logging
from pymongo import MongoClient, errors
from shared.custom_dotenv import load_env_variables

load_env_variables()

class Database:
    client = None
    db = None

    @classmethod
    def initialize(cls):
        use_remote_db = os.getenv('USE_REMOTE_DB', 'False').lower() in ['true', '1', 't']
        uri = os.getenv('MONGODB_URI_REMOTE') if use_remote_db else os.getenv('MONGODB_URI_LOCAL')
        db_name = 'BuildingReportsDB'
        
        try:
            cls.client = MongoClient(uri, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)
            cls.client.server_info()  # Trigger exception if connection fails
            cls.db = cls.client[db_name]
            logging.info("Connected to MongoDB")
        except errors.ServerSelectionTimeoutError as err:
            logging.error(f"Could not connect to MongoDB: {err}")
            raise
        except errors.ConnectionFailure as err:
            logging.error(f"Connection Failure: {err}")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise

    @classmethod
    def get_collection(cls, name):
        return cls.db[name]

# Initialize the database globally
# Initialize the database instance
Database.initialize()
db_instance = Database