from fastapi import FastAPI
from app.modules.radius.router import router as radius_router
from app.core.config import settings
from app.modules.users.routes import router


app = FastAPI(title="ISP Backend")

app.include_router(radius_router, prefix="/radius")
