# Audit Log Models
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

class ActionType(Enum):
    CHAT_MESSAGE = "chat_message"
    TELEMETRY_COLLECTED = "telemetry_collected"
    TOOL_EXECUTED = "tool_executed"
    SCREENSHOT_ANALYZED = "screenshot_analyzed"
    DEEP_LINK_TRIGGERED = "deep_link_triggered"
    HITL_APPROVED = "hitl_approved"
    HITL_DENIED = "hitl_denied"

class AuditEvent(BaseModel):
    event_id: str
    user_id: str
    session_id: str
    action_type: ActionType
    timestamp: datetime
    details: Dict[str, Any]
    pii_detected: bool = False
    pii_redacted: bool = False

class AuditLog:
    """Simple in-memory audit log (in production, use database)"""

    def __init__(self):
        self.events: list[AuditEvent] = []

    def log(self, event: AuditEvent):
        self.events.append(event)
        # In production, persist to database here

    def get_user_events(self, user_id: str, limit: int = 100) -> list[AuditEvent]:
        return [e for e in self.events if e.user_id == user_id][:limit]

audit_log = AuditLog()
