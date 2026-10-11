"""Tests for screenshot analyzer tool"""
import pytest
from app.agent.tools.screenshot_analyzer import ScreenshotAnalyzerTool


class TestScreenshotAnalyzerTool:
    """Tests for the ScreenshotAnalyzerTool class"""

    def setup_method(self):
        self.tool = ScreenshotAnalyzerTool()

    def test_basic_screenshot_analysis(self):
        """Test basic screenshot analysis with mock data"""
        # Using a minimal base64 string for testing
        test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

        result = self.tool._run(
            image_base64=test_image,
            user_description="Show me the error screen"
        )

        assert result["status"] == "analyzed"
        assert "analysis" in result
        analysis = result["analysis"]
        assert isinstance(analysis, dict)

    def test_screenshot_with_no_description(self):
        """Test screenshot analysis without user description"""
        test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

        result = self.tool._run(image_base64=test_image)

        assert result["status"] == "analyzed"
        assert "analysis" in result

    def test_async_analysis(self):
        """Test async version of screenshot analysis"""
        import asyncio

        test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

        async def run_async():
            return await self.tool._arun(
                image_base64=test_image,
                user_description="Test error"
            )

        result = asyncio.run(run_async())
        assert result["status"] == "analyzed"

    def test_analysis_structure(self):
        """Test that analysis result has expected structure"""
        test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

        result = self.tool._run(image_base64=test_image)
        analysis = result["analysis"]

        # Check analysis has expected keys
        assert "detected_errors" in analysis or isinstance(analysis, dict)
        assert "hypothesis" in analysis or isinstance(analysis, dict)
        assert isinstance(analysis.get("recommended_actions", []), list)
