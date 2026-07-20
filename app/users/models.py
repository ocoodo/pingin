from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Model


class User(Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[int] = mapped_column(unique=True)
    password_hash: Mapped[str]
    
    sessions: Mapped[list["Session"]] = relationship(back_populates='user')
