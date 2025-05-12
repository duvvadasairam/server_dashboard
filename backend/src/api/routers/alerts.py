from fastapi import APIRouter, HTTPException
from src.api.schemas.alert import AlertCount
# This will be a mock service for now

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/count", response_model=AlertCount)
async def get_alert_counts():
    """Retrieve counts of critical, trouble, and clear alerts."""
    # Mock data as per UI example
    return AlertCount(critical=2, trouble=5, clear=5)
