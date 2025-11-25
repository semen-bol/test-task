from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from collections.abc import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
Session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise