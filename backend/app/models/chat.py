# Chat Models
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageMetadata(BaseModel):
    action: Optional[str] = None
    screenshot: Optional[str] = None
    tools_used: Optional[List[str]] = None
    actions: Optional[List[Dict[str, Any]]] = None
    requires_approval: Optional[bool] = False


class Message(BaseModel):
    id: str
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[MessageMetadata] = None


class ChatSession(BaseModel):
    id: str
    messages: List[Message] = Field(default_factory=list)
    device_telemetry: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CreateSessionRequest(BaseModel):
    user_id: str
    initial_message: Optional[str] = None
    device_telemetry: Optional[Dict[str, Any]] = None


class CreateSessionResponse(BaseModel):
    session_id: str
    status: str


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    user_id: str
    message: str
    device_telemetry: Optional[Dict[str, Any]] = None
    screenshot_base64: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    message: str
    actions: Optional[List[Dict[str, Any]]] = None
    requires_approval: bool = False
