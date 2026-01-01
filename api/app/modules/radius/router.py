from fastapi import APIRouter
from app.modules.radius.schemas import (
    RadiusAuthRequest,
    RadiusAuthResponse
)
from app.modules.radius.service import radius_auth

router = APIRouter()


@router.post("/auth", response_model=RadiusAuthResponse)
async def auth(payload: RadiusAuthRequest):
    return radius_auth(
        username=payload.username,
        mac=payload.mac,
        ip=payload.ip
    )


@router.post("/accounting")
async def accounting(payload: dict):
    print("ACCOUNTING:", payload)
    return {"status": "ok"}
