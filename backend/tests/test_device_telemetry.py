"""Tests for device telemetry tools"""
import pytest
from app.agent.tools.device_telemetry import DeviceTelemetryTool


class TestDeviceTelemetryTool:
    """Tests for the DeviceTelemetryTool class"""

    def setup_method(self):
        self.tool = DeviceTelemetryTool()

    def test_low_battery_detection(self):
        """Test detection of critically low battery"""
        telemetry = {
            "battery": {"level": 0.15, "isCharging": False},
            "storage": {"usedPercentage": 50},
            "network": {"isConnected": True, "isInternetReachable": True}
        }

        result = self.tool._run(telemetry_data=telemetry)

        assert result["status"] == "analyzed"
        assert result["issues_found"] == 1
        assert result["issues"][0]["type"] == "battery"
        assert result["issues"][0]["severity"] == "medium"

    def test_full_battery_no_issues(self):
        """Test normal battery level with no issues"""
        telemetry = {
            "battery": {"level": 0.85, "isCharging": False},
            "storage": {"usedPercentage": 50},
            "network": {"isConnected": True, "isInternetReachable": True}
        }

        result = self.tool._run(telemetry_data=telemetry)

        assert result["status"] == "analyzed"
        assert result["issues_found"] == 0
        assert result["overall_health"] == "healthy"

    def test_critical_storage_detection(self):
        """Test detection of critically low storage"""
        telemetry = {
            "battery": {"level": 0.85, "isCharging": True},
            "storage": {"usedPercentage": 95, "freeSpace": 0.5},
            "network": {"isConnected": True, "isInternetReachable": True}
        }

        result = self.tool._run(telemetry_data=telemetry)

        assert result["issues_found"] == 1
        assert result["issues"][0]["type"] == "storage"
        assert result["issues"][0]["severity"] == "high"

    def test_high_storage_warning(self):
        """Test warning for high storage usage"""
        telemetry = {
            "battery": {"level": 0.85, "isCharging": True},
            "storage": {"usedPercentage": 78, "freeSpace": 2.5},
            "network": {"isConnected": True, "isInternetReachable": True}
        }

        result = self.tool._run(telemetry_data=telemetry)

        assert result["issues_found"] == 1
        assert result["issues"][0]["type"] == "storage"
        assert result["issues"][0]["severity"] == "medium"

    def test_no_internet_detection(self):
        """Test detection of no internet connection"""
        telemetry = {
            "battery": {"level": 0.85, "isCharging": True},
            "storage": {"usedPercentage": 50},
            "network": {"isConnected": True, "isInternetReachable": False}
        }

        result = self.tool._run(telemetry_data=telemetry)

        assert result["issues_found"] == 1
        assert result["issues"][0]["type"] == "network"
        assert result["issues"][0]["severity"] == "high"

    def test_no_connection_detection(self):
        """Test detection of no network connection"""
        telemetry = {
            "battery": {"level": 0.85, "isCharging": True},
            "storage": {"usedPercentage": 50},
            "network": {"isConnected": False, "isInternetReachable": False}
        }

        result = self.tool._run(telemetry_data=telemetry)

        assert result["issues_found"] == 1
        assert result["issues"][0]["type"] == "network"
        assert result["issues"][0]["severity"] == "high"

    def test_async_run(self):
        """Test async version of the tool"""
        import asyncio

        telemetry = {
            "battery": {"level": 0.10, "isCharging": False},
            "storage": {"usedPercentage": 92},
            "network": {"isConnected": False}
        }

        async def run_async():
            return await self.tool._arun(telemetry_data=telemetry)

        result = asyncio.run(run_async())
        assert result["issues_found"] >= 1
