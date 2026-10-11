# Screenshot Analyzer Tool
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class ScreenshotAnalysisInput(BaseModel):
    image_base64: str = Field(description="Base64-encoded screenshot image")
    user_description: Optional[str] = Field(
        default=None,
        description="Optional user description of what's wrong in the screenshot"
    )

class ScreenshotAnalyzerTool(BaseTool):
    name: str = "analyze_screenshot"
    description: str = """
    Analyze a screenshot to identify error messages, UI issues, or misconfigurations.
    Input: Base64-encoded image and optional user description.
    Returns: Detailed analysis of visible issues.
    """
    args_schema: type[BaseModel] = ScreenshotAnalysisInput

    def _run(self, image_base64: str, user_description: Optional[str] = None) -> Dict[str, Any]:
        """Synchronous screenshot analysis using mock data"""
        # In production, this would call Claude Vision API
        return {
            "status": "analyzed",
            "analysis": {
                "detected_errors": [],
                "screen_context": "Settings or home screen",
                "ui_issues": [],
                "hypothesis": "Issue appears to be related to user configuration or app settings",
                "recommended_actions": [
                    "Check app permissions",
                    "Verify network settings",
                    "Review recent app updates"
                ]
            },
            "requires_action": False
        }

    async def _arun(self, image_base64: str, user_description: Optional[str] = None) -> Dict[str, Any]:
        return self._run(image_base64, user_description)
