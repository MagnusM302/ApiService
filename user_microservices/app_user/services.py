# service.py
import re
import bcrypt
from user_microservices.app_user.dal import UserRepository
from user_microservices.app_user.models import User, UserRole
from user_microservices.app_user.converters import UserConverter
from user_microservices.app_user.dto import UserDTO
from shared.auth_service import JWTService

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.jwt_service = JWTService()  

    def register_user(self, name, address, post_number, phone, username, email, password, role):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        
        try:
            role_enum = UserRole[role.upper()]  # Convert role to uppercase
        except KeyError:
            raise ValueError("Invalid role specified")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = self.user_repository.create_user(name=name, address=address, post_number=post_number, phone=phone,
                                                username=username, email=email, hashed_password=hashed_password, role=role_enum)
        user_data = UserConverter.to_dto(user)
        user_data.user_id = str(user.user_id)  # Ensure user_id is converted to string in DTO
        return user_data

    def get_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        return UserConverter.to_dto(user) if user else None

    def update_user(self, user_id, update_data):
        updated_user = self.user_repository.update_user(user_id, update_data)
        return UserConverter.to_dto(updated_user) if updated_user else None

    def delete_user(self, user_id):
        return self.user_repository.delete_user(user_id)
    
    def login_user(self, username, password):
        user = self.user_repository.get_user_by_username(username)
        if user:
            password_hash = user.password_hash
            if isinstance(password_hash, str):
                password_hash = password_hash.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                role_str = user.role.name if isinstance(user.role, UserRole) else UserRole(user.role).name
                token = self.jwt_service.generate_token(user.user_id, role_str)
                return {"token": token, "user_id": str(user.user_id), "role": role_str}
        raise ValueError("Invalid username or password")
