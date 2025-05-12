from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.models.database import ServerStatus # Import the ServerStatus enum

class Server(BaseModel):
    id: int
    name: str
    ip_address: str
    created_at: datetime
    tag: str
    provider: str
    status: ServerStatus # Use the ServerStatus enum directly

    model_config = ConfigDict(from_attributes=True)
