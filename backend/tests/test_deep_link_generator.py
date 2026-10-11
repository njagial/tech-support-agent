"""Tests for deep link generator tool"""
import pytest
from app.agent.tools.deep_link_generator import DeepLinkGeneratorTool


class TestDeepLinkGeneratorTool:
    """Tests for the DeepLinkGeneratorTool class"""

    def setup_method(self):
        self.tool = DeepLinkGeneratorTool()

    def test_wifi_deep_link_ios(self):
        """Test generating Wi-Fi deep link for iOS"""
        result = self.tool._run(issue_type="wifi", platform="ios")

        assert result["platform"] == "ios"
        assert result["issue_type"] == "wifi"
        assert "deep_link" in result
        assert "App-Prefs:WIFI" in result["deep_link"]
        assert "label" in result
        assert "instruction" in result

    def test_battery_deep_link_ios(self):
        """Test generating battery deep link for iOS"""
        result = self.tool._run(issue_type="battery", platform="ios")

        assert result["platform"] == "ios"
        assert "BATTERY_USAGE" in result["deep_link"]

    def test_storage_deep_link_ios(self):
        """Test generating storage deep link for iOS"""
        result = self.tool._run(issue_type="storage", platform="ios")

        assert result["platform"] == "ios"
        assert "STORAGE_MGMT" in result["deep_link"]

    def test_wifi_deep_link_android(self):
        """Test generating Wi-Fi deep link for Android"""
        result = self.tool._run(issue_type="wifi", platform="android")

        assert result["platform"] == "android"
        assert result["issue_type"] == "wifi"
        assert "WIFI_SETTINGS" in result["deep_link"]
        assert "label" in result

    def test_battery_deep_link_android(self):
        """Test generating battery deep link for Android"""
        result = self.tool._run(issue_type="battery", platform="android")

        assert result["platform"] == "android"
        assert "BATTERY_SAVER_SETTINGS" in result["deep_link"]

    def test_storage_deep_link_android(self):
        """Test generating storage deep link for Android"""
        result = self.tool._run(issue_type="storage", platform="android")

        assert result["platform"] == "android"
        assert "INTERNAL_STORAGE_SETTINGS" in result["deep_link"]

    def test_invalid_issue_type_ios(self):
        """Test handling of invalid issue type for iOS"""
        result = self.tool._run(issue_type="invalid_issue", platform="ios")

        assert "error" in result

    def test_invalid_issue_type_android(self):
        """Test handling of invalid issue type for Android"""
        result = self.tool._run(issue_type="invalid_issue", platform="android")

        assert "error" in result

    def test_async_deep_link(self):
        """Test async version of deep link generation"""
        import asyncio

        async def run_async():
            return await self.tool._arun(issue_type="wifi", platform="ios")

        result = asyncio.run(run_async())
        assert "deep_link" in result
