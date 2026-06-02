from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.settings import settings

engine = create_async_engine(settings.db_url)
session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


class Model(DeclarativeBase):
    pass