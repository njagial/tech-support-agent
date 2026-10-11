# Validators
from typing import Any, Dict
import re

class Validators:
    """Input validation utilities"""

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone number format"""
        # Remove common separators for validation
        cleaned = re.sub(r'[\s\-\.\(\)]', '', phone)
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, cleaned))

    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize user text input"""
        # Remove potentially harmful characters
        return re.sub(r'[<>&\'"]', '', text)

    @staticmethod
    def validate_image_base64(image_data: str) -> bool:
        """Validate base64 image data"""
        if not image_data:
            return False
        # Basic check - should be valid base64
        try:
            import base64
            base64.b64decode(image_data)
            return True
        except:
            return False

    @staticmethod
    def validate_telemetry(data: Dict[str, Any]) -> bool:
        """Validate telemetry data structure"""
        required_fields = ["device", "battery", "storage", "network", "timestamp"]
        return all(field in data for field in required_fields)

    @staticmethod
    def is_within_size_limit(data: str, max_mb: int = 5) -> bool:
        """Check if data is within size limit"""
        return len(data.encode('utf-8')) <= max_mb * 1024 * 1024

def validate_chat_request(data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate chat request payload"""
    if not data.get("message"):
        return False, "Message is required"
    if not data.get("user_id"):
        return False, "User ID is required"
    if len(data.get("message", "")) > 5000:
        return False, "Message too long"
    return True, ""
