class CustomBaseException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class GenericException(CustomBaseException):
    pass

class AlreadyExistsException(CustomBaseException):
    pass

class NotFoundException(CustomBaseException):
    pass