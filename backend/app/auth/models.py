from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime

from app.database import Model


class Session(Model):
    __tablename__ = 'sessions'
    
    session_id: Mapped[str] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    
    account = relationship('Account', back_populates='sessions')
