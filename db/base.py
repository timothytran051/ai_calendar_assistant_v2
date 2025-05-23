# from sqlalchemy.orm import declarative_base, relationship
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import session, declarative_base, sessionmaker
# from fastapi import Depends
# from typing import AsyncGenerator

# Base = declarative_base()

# #URL = 

# engine = create_async_engine(URL, echo=true)

# async_session = sessionmaker(
#     bind = engine,
#     class_ = AsyncSession,
#     expire_on_commit = False
# )

# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session() as session:
#         yield session