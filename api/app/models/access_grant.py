import uuid
from sqlalchemy import (
    Column, Boolean, TIMESTAMP, Text, Integer, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.models.base import Base


class AccessGrant(Base):
    __tablename__ = "access_grants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    router_id = Column(UUID(as_uuid=True), ForeignKey("routers.id"), nullable=False)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    start_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)

    rate_limit = Column(Text)
    session_timeout = Column(Integer)
    idle_timeout = Column(Integer)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
