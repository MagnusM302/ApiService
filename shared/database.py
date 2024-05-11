from pymongo import MongoClient

class Database:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['property_reports_db']

    @staticmethod
    def get_collection(name):
        return Database.db[name]
