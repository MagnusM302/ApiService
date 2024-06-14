# i_user_service.py
from abc import ABC, abstractmethod
from user_microservices.app_user.dto.user_dto import UserDTO

class IUserService(ABC):

    @abstractmethod
    def register_user(self, name, address, post_number, phone, username, email, password, role) -> UserDTO:
        pass

    @abstractmethod
    def get_user(self, user_id) -> UserDTO:
        pass

    @abstractmethod
    def update_user(self, user_id, update_data) -> UserDTO:
        pass

    @abstractmethod
    def delete_user(self, user_id) -> bool:
        pass

    @abstractmethod
    def login_user(self, username, password) -> dict:
        pass
