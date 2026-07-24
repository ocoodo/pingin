class AlreadyInUseError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidSessionError(Exception):
    pass


class NotFoundError(Exception):
    pass


class ForbiddenError(Exception):
    pass
