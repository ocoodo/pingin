from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.settings import settings


engine = create_async_engine(settings.db_url, echo=True)
session_factory = async_sessionmaker(engine, expire_on_commit=False)
Model = declarative_base()


async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session
