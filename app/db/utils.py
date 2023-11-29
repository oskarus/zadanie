from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database
from settings import config


database = Database(config.database_url)
Base = declarative_base()

engine = create_async_engine(config.database_url, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
