from pydantic import BaseModel
from typing import Optional


class RadiusAuthRequest(BaseModel):
    username: str
    mac: str
    ip: str


class RadiusAuthResponse(BaseModel):
    allow: bool
    timeout: Optional[int] = None
    rate: Optional[str] = None
