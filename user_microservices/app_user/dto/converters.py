from user_microservices.app_user.models.user import User
from user_microservices.app_user.models.user_role import UserRole
from user_microservices.app_user.dto.user_dto import UserDTO


class UserConverter:
    @staticmethod
    def to_dto(user):
        """Converts a User instance into a UserDTO instance, safely excluding sensitive data."""
        if not isinstance(user, User):
            raise ValueError("Provided object is not a User instance")
        
        return UserDTO(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            role=user.role.name if user.role else "No Role"  # Convert enum to string here
        )

    @staticmethod
    def from_dto(dto, password_hash=None):
        """Converts a UserDTO instance back into a User instance, requires password hash for complete model."""
        if not isinstance(dto, UserDTO):
            raise ValueError("Provided object is not a UserDTO instance")
        
        return User(
            _id=dto.user_id,
            name=dto.name,
            email=dto.email,
            role=UserRole[dto.role] if dto.role and dto.role in UserRole._member_names_ else None,
            password_hash=password_hash  # Assumed to be handled securely elsewhere
        )