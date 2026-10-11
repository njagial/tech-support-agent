# Agent State Definitions
from typing import Literal, Optional, List, TypedDict, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class DeviceTelemetry(BaseModel):
    """Device telemetry data from mobile client"""
    device: Dict[str, Any]
    battery: Dict[str, Any]
    storage: Dict[str, Any]
    memory: Dict[str, Any]
    network: Dict[str, Any]
    timestamp: datetime


class ConversationMessage(BaseModel):
    """Single message in the conversation"""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class ToolExecution(BaseModel):
    """Record of a tool execution"""
    tool_name: str
    input_params: Dict[str, Any]
    output: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    success: bool


class AgentState(TypedDict):
    """LangGraph state for tech support agent"""
    # Conversation context
    messages: List[ConversationMessage]
    user_id: str
    session_id: str

    # Diagnostic context
    device_telemetry: Optional[DeviceTelemetry]
    screenshot_analysis: Optional[Dict[str, Any]]
    kb_search_results: Optional[List[Dict[str, Any]]]

    # Tool execution tracking
    tool_executions: List[ToolExecution]

    # Agent reasoning
    current_hypothesis: Optional[str]
    recommended_actions: List[Dict[str, Any]]
    requires_hitl_approval: bool

    # Workflow state
    next_step: Literal[
        "collect_telemetry",
        "request_screenshot",
        "search_kb",
        "analyze_symptoms",
        "generate_solution",
        "await_hitl",
        "end"
    ]
