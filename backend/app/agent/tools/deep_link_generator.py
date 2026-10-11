# Deep Link Generator Tool
from typing import Dict, Any, Literal


class DeepLinkGeneratorTool:
    """Generate deep links to open native OS settings for troubleshooting"""

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

    def generate(self, issue_type: str, platform: Literal["ios", "android"]) -> Dict[str, Any]:
        """Generate a deep link for the issue type"""
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

    async def generate_async(self, issue_type: str, platform: Literal["ios", "android"]) -> Dict[str, Any]:
        """Async version"""
        return self.generate(issue_type, platform)
