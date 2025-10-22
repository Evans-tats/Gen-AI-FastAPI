from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from DB_Model import Base
from fastapi import Depends
from typing import Annotated

database_url = "postgresql+psycopg://fastapi:mysecretpassword@localhost:5432/backend_db"
engine = create_async_engine(database_url,echo=True)

async def init_db() ->None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

sessionLocal = async_sessionmaker(
    bind=engine, autoflush=False, autocommit=False, class_=AsyncSession
)

async def get_db_session():
    try:
        async with sessionLocal as session:
            yield session
    except:
        await session.rollback()
    finally:
        await session.close()

DBSession = Annotated[AsyncSession, Depends(get_db_session)]