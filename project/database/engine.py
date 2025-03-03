from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from database.config import DB_CONFIG
from database.model import Model

engine = create_async_engine(
    DB_CONFIG.url,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

# async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(Model.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(
        engine, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

# async def create_tables():
#     """"""
#     async with engine.begin() as connection:
#         await connection.run_sync(Model.metadata.create_all)
#
#
# async def delete_tables():
#     """"""
#     async with engine.begin() as connection:
#         await connection.run_sync(Model.metadata.drop_all)
