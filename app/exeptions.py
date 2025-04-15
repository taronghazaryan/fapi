class UserNotFoundError(Exception):
    pass

class APIIntegrationError(Exception):
    pass

class InvalidActionError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class PasswordMismatch(Exception):
    pass