# Deep Link Generator Tool
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Any, Literal

class DeepLinkInput(BaseModel):
    issue_type: str = Field(description="Type of issue: wifi, battery, storage, permissions, etc.")
    platform: Literal["ios", "android"] = Field(description="Target mobile platform")

class DeepLinkGeneratorTool(BaseTool):
    name: str = "generate_deep_link"
    description: str = """
    Generate a deep link to open native OS settings for troubleshooting.
    Input: Issue type and platform.
    Returns: Deep link URI and user-facing instructions.
    """
    args_schema: type[BaseModel] = DeepLinkInput

    IOS_LINKS = {
        "wifi": {"uri": "App-Prefs:WIFI", "label": "Wi-Fi Settings"},
        "bluetooth": {"uri": "App-Prefs:Bluetooth", "label": "Bluetooth Settings"},
        "battery": {"uri": "App-Prefs:BATTERY_USAGE", "label": "Battery Settings"},
        "storage": {"uri": "App-Prefs:General&path=STORAGE_MGMT", "label": "Storage Management"},
        "cellular": {"uri": "App-Prefs:MOBILE_DATA", "label": "Cellular Data"},
        "permissions": {"uri": "app-settings:", "label": "App Permissions"},
        "notifications": {"uri": "App-Prefs:NOTIFICATIONS_ID", "label": "Notifications"},
    }

    ANDROID_LINKS = {
        "wifi": {"intent": "android.settings.WIFI_SETTINGS", "label": "Wi-Fi Settings"},
        "bluetooth": {"intent": "android.settings.BLUETOOTH_SETTINGS", "label": "Bluetooth Settings"},
        "battery": {"intent": "android.settings.BATTERY_SAVER_SETTINGS", "label": "Battery Settings"},
        "storage": {"intent": "android.settings.INTERNAL_STORAGE_SETTINGS", "label": "Storage Management"},
        "cellular": {"intent": "android.settings.DATA_ROAMING_SETTINGS", "label": "Mobile Data"},
        "permissions": {"intent": "android.settings.APPLICATION_DETAILS_SETTINGS", "label": "App Info"},
        "notifications": {"intent": "android.settings.APP_NOTIFICATION_SETTINGS", "label": "Notifications"},
    }

    def _run(self, issue_type: str, platform: Literal["ios", "android"]) -> Dict[str, Any]:
        if platform == "ios":
            link_data = self.IOS_LINKS.get(issue_type)
            if not link_data:
                return {"error": f"No iOS deep link found for issue type: {issue_type}"}

            return {
                "platform": "ios",
                "issue_type": issue_type,
                "deep_link": link_data["uri"],
                "label": link_data["label"],
                "instruction": f"Tap the button below to open {link_data['label']}"
            }
        else:
            link_data = self.ANDROID_LINKS.get(issue_type)
            if not link_data:
                return {"error": f"No Android intent found for issue type: {issue_type}"}

            return {
                "platform": "android",
                "issue_type": issue_type,
                "deep_link": f"intent://#Intent;action={link_data['intent']};end",
                "label": link_data["label"],
                "instruction": f"Tap the button below to open {link_data['label']}"
            }

    async def _arun(self, issue_type: str, platform: Literal["ios", "android"]) -> Dict[str, Any]:
        return self._run(issue_type, platform)
