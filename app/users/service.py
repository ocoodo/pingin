from app.users.schemas import UserOut
from app.users.repo import UserRepo
from app.exceptions import AlreadyInUseError
from app.utils import hash_password


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo
    
    async def new_user(self, username: str, password: str) -> UserOut:
        exists = await self.repo.get_by_username(username)
        if exists:
            raise AlreadyInUseError
        
        password_hash = hash_password(password)
        user = await self.repo.add(username, password_hash)
        return UserOut(
            id=user.id,
            username=user.username
        )