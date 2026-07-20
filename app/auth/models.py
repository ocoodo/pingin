from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database import Model
from app.types import TZDateTime


class Session(Model):
    __tablename__ = 'sessions'
    
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    expires_at: Mapped[datetime] = mapped_column(TZDateTime)
    
    user: Mapped["User"] = relationship(back_populates='sessions')