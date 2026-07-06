from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncIterator

engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True,
        connect_args={"ssl": True}
    )
)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all) #this will automatically create tables using metadata from models that were created using SQLModel

async def get_session() -> AsyncIterator[AsyncSession]:
    Sesssion = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with Sesssion() as session:
        yield session

 