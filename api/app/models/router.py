import uuid
from sqlalchemy import Column, Text, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.sql import func

from app.models.base import Base


class Router(Base):
    __tablename__ = "routers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(Text, nullable=False)
    site_name = Column(Text, nullable=False)

    wan_public_ip = Column(INET, nullable=True)
    lan_ip = Column(INET, nullable=True)

    radius_secret = Column(Text, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
