from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Model


class Account(Model):
    __tablename__ = 'accounts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    
    sessions = relationship('Session', back_populates='account')