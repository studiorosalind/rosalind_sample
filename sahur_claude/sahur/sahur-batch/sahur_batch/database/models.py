from datetime import datetime
import uuid

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship

from sahur_batch.database.connection import Base


class Issue(Base):
    """Database model for issues."""
    __tablename__ = "issues"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    source = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    event_transaction_id = Column(String(255), nullable=True)
    additional_metadata = Column(JSON, nullable=True)

    # Relationships
    tracking = relationship("IssueTracking", back_populates="issue", uselist=False)
    messages = relationship("IssueMessage", back_populates="issue")


class IssueTracking(Base):
    """Database model for issue tracking."""
    __tablename__ = "issue_tracking"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    issue_id = Column(String(36), ForeignKey("issues.id"), nullable=False)
    status = Column(String(50), nullable=False)
    batch_process_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cause_context = Column(JSON, nullable=True)
    history_context = Column(JSON, nullable=True)
    solution = Column(JSON, nullable=True)
    
    # Relationships
    issue = relationship("Issue", back_populates="tracking")


class IssueMessage(Base):
    """Database model for issue messages."""
    __tablename__ = "issue_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    issue_id = Column(String(36), ForeignKey("issues.id"), nullable=False)
    role = Column(String(50), nullable=False)  # system, user, assistant
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    issue = relationship("Issue", back_populates="messages")
