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

        # Improved role handling
        if isinstance(role, str):
            try:
                self.role = UserRole[role]
            except KeyError:
                raise ValueError(f"Invalid role specified: {role}")
        elif isinstance(role, int):
            try:
                self.role = UserRole(role)  # Assuming integer maps directly to the enum
            except ValueError:
                raise ValueError(f"Invalid role index specified: {role}")
        elif isinstance(role, UserRole):
            self.role = role
        else:
            raise TypeError("Role must be a UserRole enum, its string key, or its integer index.")

    def __str__(self):
        role_name = self.role.name if self.role else "No Role"
        return f"User({self.email}, Role: {role_name})"
