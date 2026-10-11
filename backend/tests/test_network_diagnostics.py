"""Tests for network diagnostics tool"""
import pytest
from app.agent.tools.network_diagnostics import NetworkDiagnosticsTool


class TestNetworkDiagnosticsTool:
    """Tests for the NetworkDiagnosticsTool class"""

    def setup_method(self):
        self.tool = NetworkDiagnosticsTool()

    def test_no_internet_detection(self):
        """Test detection of no internet connection"""
        telemetry = {
            "network": {"isConnected": True, "isInternetReachable": False}
        }

        result = self.tool._run(telemetry_data=telemetry)

        assert result["status"] == "analyzed"
        assert len(result["issues"]) > 0
        assert result["issues"][0]["type"] == "no_internet"
        assert result["issues"][0]["severity"] == "high"

    def test_no_connection_detection(self):
        """Test detection of no network connection"""
        telemetry = {
            "network": {"isConnected": False}
        }

        result = self.tool._run(telemetry_data=telemetry)

        assert len(result["issues"]) > 0
        assert result["issues"][0]["type"] == "no_connection"

    def test_normal_connection_no_issues(self):
        """Test normal connection with no issues"""
        telemetry = {
            "network": {"isConnected": True, "isInternetReachable": True}
        }

        result = self.tool._run(telemetry_data=telemetry)

        assert len(result["issues"]) == 0
        assert len(result["recommendations"]) == 0

    def test_recommendations_provided(self):
        """Test that recommendations are provided for issues"""
        telemetry = {
            "network": {"isConnected": False}
        }

        result = self.tool._run(telemetry_data=telemetry)

        assert len(result["recommendations"]) > 0

    def test_async_run(self):
        """Test async version of the tool"""
        import asyncio

        telemetry = {
            "network": {"isConnected": False}
        }

        async def run_async():
            return await self.tool._arun(telemetry_data=telemetry)

        result = asyncio.run(run_async())
        assert "issues" in result
