import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load .env from the 'backend' directory
# Assumes database.py is in backend/src/, so .env is two levels up from __file__
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set or .env file not found/loaded correctly from backend/.env")

engine = create_async_engine(DATABASE_URL) # echo=True can be added for debugging SQL

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """
    FastAPI dependency to get an async database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit() # Commit the transaction if all operations within the request were successful
        except Exception:
            await session.rollback() # Rollback in case of any exception
            raise
        finally:
            await session.close()
