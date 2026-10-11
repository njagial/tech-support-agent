# PII Filter Service
import re
from typing import List, Dict, Any
import hashlib

class PIIFilter:
    """Server-side PII detection and redaction"""

    PATTERNS = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b(\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "password": r"(?i)(password|passwd|pwd)\s*[=:]\s*\S+",
    }

    def __init__(self):
        self.compiled_patterns = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in self.PATTERNS.items()
        }

    def detect_pii(self, text: str) -> Dict[str, Any]:
        """Detect PII in text content"""
        found_types = []

        for pii_type, pattern in self.compiled_patterns.items():
            matches = pattern.findall(text)
            if matches:
                found_types.append(pii_type)

        return {
            "has_pii": len(found_types) > 0,
            "pii_types": found_types,
            "match_count": len(found_types)
        }

    def redact_text(self, text: str) -> str:
        """Redact PII from text"""
        redacted = text
        for pattern in self.compiled_patterns.values():
            redacted = pattern.sub("[REDACTED]", redacted)
        return redacted

    def hash_user_id(self, user_id: str) -> str:
        """Hash user ID for privacy-preserving tracking"""
        return hashlib.sha256(user_id.encode()).hexdigest()[:16]

    def filter_screenshot_content(self, ocr_text: str) -> Dict[str, Any]:
        """Process OCR text from screenshots"""
        detection = self.detect_pii(ocr_text)

        return {
            "detected": detection["has_pii"],
            "pii_types": detection["pii_types"],
            "should_redact": detection["has_pii"],
            "redacted_text": self.redact_text(ocr_text) if detection["has_pii"] else ocr_text
        }

def get_pii_filter() -> PIIFilter:
    return PIIFilter()
