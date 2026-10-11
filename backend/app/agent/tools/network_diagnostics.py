# Network Diagnostics Tool
from langchain.tools import BaseTool
from typing import Dict, Any
from pydantic import BaseModel, Field

class NetworkDiagnosticsInput(BaseModel):
    telemetry_data: Dict[str, Any]

class NetworkDiagnosticsTool(BaseTool):
    name: str = "analyze_network_diagnostics"
    description: str = "Analyze network connectivity issues including latency and DNS resolution"
    args_schema: type[BaseModel] = NetworkDiagnosticsInput

    def _run(self, telemetry_data: Dict[str, Any]) -> Dict[str, Any]:
        network = telemetry_data.get("network", {})
        issues = []

        if not network.get("isConnected", True):
            issues.append({
                "type": "no_connection",
                "severity": "high",
                "message": "No network connectivity",
                "action": "check_network_settings"
            })

        if network.get("isInternetReachable") == False:
            issues.append({
                "type": "no_internet",
                "severity": "high",
                "message": "Connected to network but no internet access",
                "action": "diagnose_network"
            })

        return {
            "status": "analyzed",
            "issues": issues,
            "recommendations": [
                "Check if Wi-Fi or mobile data is enabled",
                "Try reconnecting to the network",
                "Restart the device if issues persist"
            ] if issues else []
        }

    async def _arun(self, telemetry_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._run(telemetry_data)
