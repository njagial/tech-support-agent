# Network Diagnostics Tool
from typing import Dict, Any


class NetworkDiagnosticsTool:
    """Analyze network connectivity issues"""

    def analyze(self, telemetry_data: Dict[str, Any]) -> Dict[str, Any]:
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

    async def analyze_async(self, telemetry_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.analyze(telemetry_data)
