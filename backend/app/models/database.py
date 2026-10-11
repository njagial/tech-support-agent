# Database Models
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    sessions = relationship("ChatSession", back_populates="user")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("chat_sessions.id", ondelete="CASCADE"))
    role = Column(String)  # user, assistant, system
    content = Column(Text)
    metadata = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    session_id = Column(String)
    action_type = Column(String)
    details = Column(JSON)
    pii_detected = Column(Boolean, default=False)
    pii_redacted = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class KBDocument(Base):
    __tablename__ = "kb_documents"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    source = Column(String)
    category = Column(String)
    os = Column(String)  # ios, android, both
    created_at = Column(DateTime, default=datetime.utcnow)
    vector_id = Column(String)  # For vector store lookup
