from pydantic import BaseModel

class AlertCount(BaseModel):
    critical: int
    trouble: int
    clear: int

class AlertMessage(BaseModel):
    message: str
