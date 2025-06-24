from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from ..models.tables import Base
from ..db.config import settings



engine = create_async_engine(settings.db_url)
new_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        



