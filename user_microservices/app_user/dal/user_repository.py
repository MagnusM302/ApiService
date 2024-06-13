from bson.objectid import ObjectId
from user_microservices.app_user.models.user_role import UserRole
from user_microservices.app_user.models import User
from user_microservices.app_user.dal.i_user_repository import IUserRepository
from shared.database import Database

class UserRepository(IUserRepository):
    
    def __init__(self, db: Database):
        self.collection = db.get_collection('users')
    def create_user(self, name, address, post_number, phone, username, email, hashed_password, role):
        """
        Create a new user in the database.
        Ensure 'role' is an instance of UserRole.
        """
        user_data = {
            "name": name,
            "address": address,
            "post_number": post_number,
            "phone": phone,
            "username": username,
            "email": email,
            "password_hash": hashed_password,
            "role": role.name  # Store role as string
        }
        result = self.collection.insert_one(user_data)
        user_data['_id'] = str(result.inserted_id)
        return User(**user_data)  # Return a user object instead of just an ID

    def get_user_by_id(self, user_id):
        document = self.collection.find_one({"_id": ObjectId(user_id)})
        if document:
            return User(**document)
        return None

    def get_user_by_username(self, username):
        document = self.collection.find_one({"username": username})
        if document:
            return User(**document)
        return None

    def update_user(self, user_id, update_data):
        result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        return result.modified_count > 0

    def delete_user(self, user_id):
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
