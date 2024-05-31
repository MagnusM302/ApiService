# user_microservices/app_user/repository.py

from bson.objectid import ObjectId
from shared.database import Database
from user_microservices.app_user.enums import UserRole
from user_microservices.app_user.models import User
from enum import Enum

class UserRepository:
    def __init__(self):
        self.collection = Database.get_collection('users')

    def create_user(self, name, address, post_number, phone, username, email, hashed_password, role):
        if not isinstance(role, UserRole):
            raise ValueError("Role must be an instance of UserRole")
        
        user_data = {
            "name": name,
            "address": address,
            "post_number": post_number,
            "phone": phone,
            "username": username,
            "email": email,
            "password_hash": hashed_password,
            "role": role.value
        }
        result = self.collection.insert_one(user_data)
        user_data['user_id'] = str(result.inserted_id)
        del user_data['_id']  # Remove _id key
        return User(**user_data)

    def get_user_by_id(self, user_id):
        document = self.collection.find_one({"_id": ObjectId(user_id)})
        if document:
            document['user_id'] = str(document['_id'])
            document['role'] = UserRole(document['role'])
            del document['_id']  # Remove _id key
            return User(**document)
        return None

    def get_user_by_username(self, username):
        print(f"Attempting to find user by username: {username}")
        document = self.collection.find_one({"username": username})
        if document:
            print(f"User found: {document}")
            document['user_id'] = str(document['_id'])
            document['role'] = UserRole(document['role'])
            del document['_id']  # Remove _id key
            user = User(**document)
            print(f"User loaded: {user.username}, Role: {user.role.name}")
            return user
        else:
            print("No user found with that username.")
        return None



    def update_user(self, user_id, update_data):
        if 'role' in update_data and isinstance(update_data['role'], UserRole):
            update_data['role'] = update_data['role'].value
        result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        return result.modified_count > 0

    def delete_user(self, user_id):
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
