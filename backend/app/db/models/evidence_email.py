import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EvidenceEmail(Base):
    __tablename__ = "evidence_emails"
    __table_args__ = (
        UniqueConstraint(
            "provider", "provider_message_id", name="uq_evidence_provider_message"
        ),
        Index("ix_evidence_user_domain", "user_id", "from_domain"),
        Index("ix_evidence_user_sent_at", "user_id", "sent_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    provider_message_id: Mapped[str] = mapped_column(String(255), nullable=False)
    from_address: Mapped[str] = mapped_column(String(320), nullable=False)
    from_domain: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)
    raw_headers: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="evidence_emails")
    service_links = relationship(
        "ServiceEvidenceLink", back_populates="evidence_email", cascade="all, delete-orphan"
    )
    services = relationship(
        "Service",
        secondary="service_evidence_links",
        back_populates="evidence_emails",
        viewonly=True,
    )
