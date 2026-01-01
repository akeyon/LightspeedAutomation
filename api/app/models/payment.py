import uuid
from sqlalchemy import (
    Column, Text, Integer, TIMESTAMP, Enum, ForeignKey, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum

from app.models.base import Base


class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    router_id = Column(UUID(as_uuid=True), ForeignKey("routers.id"))
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))

    phone_number = Column(Text, nullable=False)
    amount_kes = Column(Integer, nullable=False)

    merchant_request_id = Column(Text)
    checkout_request_id = Column(Text, unique=True)
    mpesa_receipt = Column(Text, unique=True)

    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    status_reason = Column(Text)

    requested_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    confirmed_at = Column(TIMESTAMP(timezone=True))

    raw_callback_json = Column(JSON)
