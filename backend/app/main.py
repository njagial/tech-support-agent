"""Pocket Tech Support Agent - FastAPI Application Entry Point"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging

from app.config import get_settings
from app.agent.orchestrator import TechSupportAgentOrchestrator
from app.agent.state import AgentState, ConversationMessage, DeviceTelemetry
import uuid
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Pocket Tech Support Agent API",
    description="AI-powered mobile tech support with multi-modal diagnostics",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent orchestrator
settings = get_settings()
agent = TechSupportAgentOrchestrator(anthropic_api_key=settings.ANTHROPIC_API_KEY)

# Request/Response models
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    user_id: str
    message: str
    device_telemetry: Optional[DeviceTelemetry] = None
    screenshot_base64: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    message: str
    actions: Optional[List[dict]] = None
    requires_approval: bool = False

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Pocket Tech Support Agent",
        "version": "1.0.0"
    }

@app.post("/api/v1/chat", response_model=ChatResponse)
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

@app.post("/api/v1/telemetry")
async def submit_telemetry(telemetry: DeviceTelemetry):
    """
    Endpoint for standalone telemetry submission
    """
    try:
        logger.info(f"Received telemetry for device {telemetry.device['deviceId']}")
        return {"status": "received", "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/screenshot/analyze")
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

@app.get("/api/v1/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session by ID (placeholder - in production would query DB)"""
    return {
        "id": session_id,
        "messages": [],
        "created_at": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
