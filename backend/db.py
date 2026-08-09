from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker , declarative_base


import os 
DATABASE_URL = os.getenv("DATABASE_URL" ,"postgresql+asyncpg://postgres:rudra@localhost/jobbot")
engine = create_async_engine(DATABASE_URL , future = True)

AsyncSessionLocal = sessionmaker(engine , class_ = AsyncSession , expire_on_commit= False)
Base = declarative_base()