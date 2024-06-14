from abc import ABC, abstractmethod
from user_microservices.app_user.models import User

class IUserRepository(ABC):

    @abstractmethod
    def create_user(self, name, address, post_number, phone, username, email, hashed_password, role) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id) -> User:
        pass

    @abstractmethod
    def get_user_by_username(self, username) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id, update_data) -> bool:
        pass

    @abstractmethod
    def delete_user(self, user_id) -> bool:
        pass
