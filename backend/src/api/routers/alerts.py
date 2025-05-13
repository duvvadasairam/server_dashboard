from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.api.schemas.alert import AlertCount
from src.models.database import Alert as AlertModel
from src.database import get_db, AsyncSessionLocal
import asyncio
import sys

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/count", response_model=AlertCount)
async def get_alert_counts(db: AsyncSession = Depends(get_db)):
    print("📥 Entered /alerts/count endpoint", flush=True)
    print("📦 DB Session Type:", type(db), flush=True)

    try:
        print("⚡ About to run query...", flush=True)
        result = await db.execute(
            select(
                AlertModel.severity,
                func.count().label("count")
            ).group_by(AlertModel.severity)
        )
        print("✅ Query executed", flush=True)

        rows = result.fetchall()
        print("📊 Query result rows:", rows, flush=True)

        # Use the fetched rows to build the counts dictionary
        counts = {row.severity.value: row.count for row in rows}

        return AlertCount(
            critical=counts.get("critical", 0),
            trouble=counts.get("trouble", 0),
            clear=counts.get("clear", 0)
        )

    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        print(f"❌ ERROR: {error_type} - {error_message}", flush=True)
        raise HTTPException(status_code=500, detail=f"Internal server error. Type: {error_type}")

async def main():
    """
    Test the get_alert_counts function by simulating a database session.
    """
    print("🚀 Starting main function to test get_alert_counts...", flush=True)
    async with AsyncSessionLocal() as session:
        try:
            # Call the get_alert_counts function directly
            result = await get_alert_counts(session)
            print("✅ Test successful. Result:", result, flush=True)
        except Exception as e:
            print(f"❌ Test failed. Error: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
