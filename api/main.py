from fastapi import FastAPI
from app.modules.radius.router import router as radius_router

app = FastAPI(title="ISP Backend")

app.include_router(radius_router, prefix="/radius")
