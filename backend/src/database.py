import os
import logging
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text  # Import the text function
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env from the 'backend' directory
# Assumes database.py is in backend/src/, so .env is two levels up from __file__
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set or .env file not found/loaded correctly from backend/.env")

engine = create_async_engine(DATABASE_URL)  # echo=True can be added for debugging SQL

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """
    FastAPI dependency to get an async database session.
    Ensures proper handling of session lifecycle with logging.
    """
    async with AsyncSessionLocal() as session:
        try:
            logger.info("🔄 Starting a new database session.")
            yield session
            await session.commit()
            logger.info("✅ Database session committed successfully.")
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Error during database session: {e}")
            raise
        finally:
            await session.close()
            logger.info("🔒 Database session closed.")

async def main():
    """
    Extract and display all rows from the 'alerts' table.
    """
    try:
        logger.info("🚀 Extracting database content...")
        async with AsyncSessionLocal() as session:
            # Replace 'alerts' with your table name
            query = text("SELECT * FROM alerts")
            result = await session.execute(query)
            
            # Fetch all rows
            rows = result.fetchall()
            
            # Log or process the rows
            for row in rows:
                logger.info(f"Row: {row}")
            
            logger.info("✅ Successfully extracted database content.")
    except Exception as e:
        logger.error(f"❌ Failed to extract database content: {e}")
    finally:
        await engine.dispose()
        logger.info("🔒 Database engine disposed.")

if __name__ == "__main__":
    asyncio.run(main())