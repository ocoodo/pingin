class NotFoundError(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidSessionError(Exception):
    pass


class ForbiddenError(Exception):
    pass