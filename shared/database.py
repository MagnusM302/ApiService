from pymongo import MongoClient

class Database:
    client = MongoClient('mongodb+srv://buildingDBuser:$Skole1234@cluster0.dezwb5i.mongodb.net/BuildingReportsDB?retryWrites=true&w=majority')
    db = client['BuildingReportsDB']

    @staticmethod
    def get_collection(name):
        return Database.db[name]
