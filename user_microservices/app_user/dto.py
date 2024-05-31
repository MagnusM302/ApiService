# user_microservices/app_user/dto.py

class UserDTO:
    def __init__(self, user_id=None, name=None, address=None, post_number=None, phone=None, username=None, email=None, role=None):
        self.user_id = user_id
        self.name = name
        self.address = address
        self.post_number = post_number
        self.phone = phone
        self.username = username
        self.email = email
        self.role = role  

    def __str__(self):
        return f"UserDTO(ID: {self.user_id}, Name: {self.name}, Address: {self.address}, Post Number: {self.post_number}, Phone: {self.phone}, Username: {self.username}, Email: {self.email}, Role: {self.role})"

    def copy(self):
        """Create a copy of this UserDTO."""
        return UserDTO(self.user_id, self.name, self.address, self.post_number, self.phone, self.username, self.email, self.role)

    def set_attributes(self, other):
        """Set the attributes of this object to match another UserDTO."""
        if not isinstance(other, UserDTO):
            raise ValueError("Other must be an instance of UserDTO")
        self.user_id = other.user_id
        self.name = other.name
        self.address = other.address
        self.post_number = other.post_number
        self.phone = other.phone
        self.username = other.username
        self.email = other.email
        self.role = other.role
