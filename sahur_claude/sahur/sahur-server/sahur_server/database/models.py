from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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


class User(Base):
    """Database model for users."""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
