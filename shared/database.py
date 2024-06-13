import os
import logging
from pymongo import MongoClient, errors
from shared.custom_dotenv import load_env_variables

load_env_variables()

class Database:
    def __init__(self):
        use_remote_db = os.getenv('USE_REMOTE_DB', 'False').lower() in ['true', '1', 't']
        self.uri = os.getenv('MONGODB_URI_REMOTE') if use_remote_db else os.getenv('MONGODB_URI_LOCAL')
        self.db_name = 'BuildingReportsDB'
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)
            self.client.server_info()  # Trigger exception if connection fails
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

    def get_collection(self, name):
        return self.client[self.db_name][name]

db_instance = Database()
