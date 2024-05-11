class UserDTO:
    def __init__(self, user_id=None, name=None, email=None, role=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role

    def __str__(self):
        role_name = self.role.name if self.role else "No Role"
        return f"UserDTO(ID: {self.user_id}, Name: {self.name}, Email: {self.email}, Role: {role_name})"

    def copy(self):
        """Create a copy of this UserDTO."""
        return UserDTO(self.user_id, self.name, self.email, self.role)

    def set_attributes(self, other):
        """Set the attributes of this object to match another UserDTO."""
        if not isinstance(other, UserDTO):
            raise ValueError("Other must be an instance of UserDTO")
        self.user_id = other.user_id
        self.name = other.name
        self.email = other.email
        self.role = other.role