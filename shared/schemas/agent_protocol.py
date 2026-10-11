# Shared Agent Protocol Types (Python)
# Synced between mobile and backend

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel
from datetime import datetime

class DeviceTelemetry(BaseModel):
    device: Dict[str, Any]
    battery: Dict[str, Any]
    storage: Dict[str, Any]
    memory: Dict[str, Any]
    network: Dict[str, Any]
    timestamp: datetime

class KBResult(BaseModel):
    title: str
    content: str
    source: str
    relevance_score: float
    os: Literal["ios", "android", "both"]
    issue_category: str

class ScreenshotAnalysis(BaseModel):
    status: str
    analysis: Dict[str, Any]
    requires_action: bool

class Action(BaseModel):
    type: str
    label: str
    description: str
    deepLink: Optional[str] = None
    icon: Optional[str] = None

class MessageMetadata(BaseModel):
    action: Optional[str] = None
    screenshot: Optional[str] = None
    tools_used: Optional[List[str]] = None
    actions: Optional[List[Action]] = None
    requires_approval: Optional[bool] = False

class Message(BaseModel):
    id: str
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime
    metadata: Optional[MessageMetadata] = None

class ToolExecution(BaseModel):
    tool_name: str
    input_params: Dict[str, Any]
    output: Dict[str, Any]
    timestamp: datetime
    success: bool

class AgentState(BaseModel):
    messages: List[Message]
    user_id: str
    session_id: str
    device_telemetry: Optional[DeviceTelemetry] = None
    screenshot_analysis: Optional[ScreenshotAnalysis] = None
    kb_search_results: Optional[List[KBResult]] = None
    tool_executions: List[ToolExecution] = []
    current_hypothesis: Optional[str] = None
    recommended_actions: List[Action] = []
    requires_hitl_approval: bool = False
    next_step: Literal[
        "collect_telemetry",
        "request_screenshot",
        "search_kb",
        "analyze_symptoms",
        "generate_solution",
        "await_hitl",
        "end"
    ]

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    user_id: str
    message: str
    device_telemetry: Optional[DeviceTelemetry] = None
    screenshot_base64: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    message: str
    actions: Optional[List[Action]] = None
    requires_approval: bool = False

class DeepLinkResponse(BaseModel):
    platform: Literal["ios", "android"]
    issue_type: str
    deep_link: str
    label: str
    instruction: str
