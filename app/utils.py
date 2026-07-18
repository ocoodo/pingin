import secrets

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return hasher.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        hasher.verify(hashed, plain)
        return True
    except VerifyMismatchError:
        return False


def generate_session_id() -> str:
    return secrets.token_urlsafe(32)