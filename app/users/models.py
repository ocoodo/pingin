from sqlalchemy.orm import Mapped, mapped_column

from app.database import Model


class User(Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[int] = mapped_column(unique=True)
    password_hash: Mapped[str]
