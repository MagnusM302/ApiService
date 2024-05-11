class ApplicationException(Exception):
    """Base class for all application-specific exceptions."""
    pass

class ResourceNotFound(ApplicationException):
    def __init__(self, resource_type, identifier):
        super().__init__(f"{resource_type} with ID {identifier} not found")
        self.resource_type = resource_type
        self.identifier = identifier
