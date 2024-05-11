# models.py
from .enums import UserRole

class User:
    def __init__(self, _id=None, name=None, address=None, post_number=None, phone=None, username=None, email=None, password_hash=None, role=None):
        self.user_id = _id
        self.name = name
        self.address = address
        self.post_number = post_number
        self.phone = phone
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = UserRole[role] if isinstance(role, str) else role

    def __str__(self):
        role_name = self.role.name if self.role else "No Role"
        return f"User({self.email}, Role: {role_name})"
