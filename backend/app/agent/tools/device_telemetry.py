# Device Telemetry Analysis Tool
from langchain.tools import BaseTool
from typing import Dict, Any
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class DeviceTelemetryInput(BaseModel):
    """Input for device telemetry analyzer"""
    telemetry_data: Dict[str, Any] = Field(description="Raw telemetry data from mobile client")

class DeviceTelemetryTool(BaseTool):
    """
    Analyzes device telemetry to identify potential issues.
    This tool processes hardware metrics and network state.
    """
    name: str = "analyze_device_telemetry"
    description: str = """
    Analyze device telemetry data to identify hardware or network issues.
    Input: Raw telemetry JSON containing battery, storage, memory, and network metrics.
    Returns: Structured analysis with identified issues and severity levels.
    """
    args_schema: type[BaseModel] = DeviceTelemetryInput

    def _run(self, telemetry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous analysis of telemetry"""
        issues = []

        # Battery analysis
        battery = telemetry_data.get("battery", {})
        if battery.get("level", 100) < 20 and not battery.get("isCharging"):
            issues.append({
                "type": "battery",
                "severity": "medium",
                "message": "Battery critically low. Connect charger.",
                "action": "deep_link:battery"
            })

        # Storage analysis
        storage = telemetry_data.get("storage", {})
        if storage.get("usedPercentage", 0) > 90:
            issues.append({
                "type": "storage",
                "severity": "high",
                "message": f"Storage critically low: {storage.get('freeSpace')}GB free",
                "action": "deep_link:storage"
            })
        elif storage.get("usedPercentage", 0) > 75:
            issues.append({
                "type": "storage",
                "severity": "medium",
                "message": f"Storage running low: {storage.get('freeSpace')}GB free",
                "action": "recommend_cleanup"
            })

        # Network analysis
        network = telemetry_data.get("network", {})
        if not network.get("isConnected"):
            issues.append({
                "type": "network",
                "severity": "high",
                "message": "No network connection detected",
                "action": "deep_link:wifi"
            })
        elif not network.get("isInternetReachable"):
            issues.append({
                "type": "network",
                "severity": "high",
                "message": "Connected to network but no internet access",
                "action": "diagnose_network"
            })

        return {
            "status": "analyzed",
            "issues_found": len(issues),
            "issues": issues,
            "overall_health": "critical" if any(i["severity"] == "high" for i in issues) else "warning" if issues else "healthy"
        }

    async def _arun(self, telemetry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Async version"""
        return self._run(telemetry_data)
