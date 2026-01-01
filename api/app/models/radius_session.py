import uuid
from sqlalchemy import Column, Text, TIMESTAMP, BigInteger, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, INET

from app.models.base import Base


class RadiusSession(Base):
    __tablename__ = "radius_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    router_id = Column(UUID(as_uuid=True), ForeignKey("routers.id"))
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))

    acct_session_id = Column(Text, nullable=False)
    username = Column(Text)

    framed_ip = Column(INET)
    nas_ip_address = Column(INET)

    start_at = Column(TIMESTAMP(timezone=True))
    last_update_at = Column(TIMESTAMP(timezone=True))
    stop_at = Column(TIMESTAMP(timezone=True))

    input_octets = Column(BigInteger)
    output_octets = Column(BigInteger)

    terminate_cause = Column(Text)

    raw_packet_json = Column(JSON)
