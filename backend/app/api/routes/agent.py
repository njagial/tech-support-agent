# API Routes - Agent Endpoints
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import logging

from app.agent.orchestrator import TechSupportAgentOrchestrator
from app.agent.state import AgentState, ConversationMessage, DeviceTelemetry
from app.models.chat import ChatRequest, ChatResponse
from app.config import get_settings
import uuid

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["agent"])

settings = get_settings()
agent = TechSupportAgentOrchestrator(anthropic_api_key=settings.ANTHROPIC_API_KEY)

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for conversational tech support
    """
    try:
        session_id = request.session_id or str(uuid.uuid4())

        initial_state: AgentState = {
            "messages": [
                ConversationMessage(
                    role="user",
                    content=request.message,
                    metadata={
                        "screenshot": request.screenshot_base64
                    } if request.screenshot_base64 else None
                )
            ],
            "user_id": request.user_id,
            "session_id": session_id,
            "device_telemetry": request.device_telemetry,
            "screenshot_analysis": None,
            "kb_search_results": None,
            "tool_executions": [],
            "current_hypothesis": None,
            "recommended_actions": [],
            "requires_hitl_approval": False,
            "next_step": "collect_telemetry"
        }

        logger.info(f"Starting agent workflow for session {session_id}")
        final_state = await agent.run(initial_state)

        assistant_messages = [
            msg for msg in final_state["messages"]
            if msg.role == "assistant" and not msg.content.startswith("[SYSTEM:")
        ]

        response_message = assistant_messages[-1].content if assistant_messages else "I'm analyzing your issue..."

        return ChatResponse(
            session_id=session_id,
            message=response_message,
            actions=final_state.get("recommended_actions"),
            requires_approval=final_state.get("requires_hitl_approval", False)
        )

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/telemetry")
async def submit_telemetry(telemetry: DeviceTelemetry):
    """
    Endpoint for standalone telemetry submission
    """
    try:
        logger.info(f"Received telemetry for device {telemetry.device['deviceId']}")
        return {"status": "received", "timestamp": telemetry.timestamp}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/screenshot/analyze")
async def analyze_screenshot(image_base64: str, description: Optional[str] = None):
    """
    Endpoint for standalone screenshot analysis
    """
    try:
        from app.agent.tools.screenshot_analyzer import ScreenshotAnalyzerTool
        tool = ScreenshotAnalyzerTool()
        result = tool._run(image_base64=image_base64, user_description=description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/deeplink")
async def trigger_deep_link(action: str, platform: str):
    """
    Trigger a deep link action
    """
    try:
        from app.agent.tools.deep_link_generator import DeepLinkGeneratorTool
        tool = DeepLinkGeneratorTool()
        result = tool._run(issue_type=action, platform=platform)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
