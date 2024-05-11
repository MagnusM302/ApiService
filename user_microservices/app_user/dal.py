from bson.objectid import ObjectId
from shared.database import Database
from enum import Enum
from models import User, UserRole  # Antager at UserRole også er en del af dine modeller

class UserRepository:
    def __init__(self):
        self.collection = Database.get_collection('users')

    def create_user(self, name, address, post_number, phone, username, email, hashed_password, role):
        """
        Create a new user in the database.
        """
        user_data = {
            "name": name,
            "address": address,
            "post_number": post_number,
            "phone": phone,
            "username": username,
            "email": email,
            "password_hash": hashed_password,  # Assume password is already hashed
            "role": role.value if isinstance(role, Enum) else role
        }
        result = self.collection.insert_one(user_data)
        user_data['_id'] = str(result.inserted_id)
        return User(**user_data)  # Return a user object instead of just an ID

    def get_user_by_id(self, user_id):
        """
        Retrieve a user by their unique ID.
        """
        document = self.collection.find_one({"_id": ObjectId(user_id)})
        if document:
            return User(**document)
        return None

    def get_user_by_username(self, username):
        """
        Retrieve a user by their username.
        """
        document = self.collection.find_one({"username": username})
        if document:
            return User(**document)
        return None

    def update_user(self, user_id, update_data):
        """
        Update user data based on the provided MongoDB ID.
        """
        result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        return result.modified_count > 0

    def delete_user(self, user_id):
        """
        Delete a user based on the provided MongoDB ID.
        """
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
