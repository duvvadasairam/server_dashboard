from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.api.schemas.server import Server as ServerSchema
from src.models.database import Server as ServerModel
from src.database import get_db

router = APIRouter(prefix="/servers", tags=["servers"])

@router.get("", response_model=List[ServerSchema])
async def get_servers(db: AsyncSession = Depends(get_db)):
    """Retrieve list of servers with details from the database."""
    try:
        result = await db.execute(select(ServerModel).order_by(ServerModel.id))
        servers_db = result.scalars().all()
        if not servers_db:
            return [] # Return empty list if no servers are found
        # Convert SQLAlchemy model instances to Pydantic schema instances
        return [ServerSchema.model_validate(server) for server in servers_db]
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        # Print detailed error to backend console
        print(f"ERROR in /servers endpoint: {error_type} - {error_message}")
        # For more detailed debugging, you might want to log the full traceback
        # import traceback
        # print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error while fetching servers. Type: {error_type}")
