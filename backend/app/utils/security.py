# Security Utilities
from cryptography.fernet import Fernet
import hashlib
import base64
from typing import Optional

class SecurityUtils:
    """Security utilities for encryption and hashing"""

    def __init__(self, encryption_key: Optional[str] = None):
        if encryption_key:
            self.key = encryption_key.encode() if isinstance(encryption_key, str) else encryption_key
        else:
            self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        """Encrypt data"""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def hash_sha256(self, data: str) -> str:
        """Hash data using SHA-256"""
        return hashlib.sha256(data.encode()).hexdigest()

    def hash_device_id(self, device_id: str) -> str:
        """Hash device ID for privacy-preserving identification"""
        return self.hash_sha256(device_id)[:16]

    def generate_session_token(self, user_id: str) -> str:
        """Generate a secure session token"""
        import secrets
        return f"{user_id}_{secrets.token_urlsafe(32)}"

    def validate_token(self, token: str, user_id: str) -> bool:
        """Validate a session token"""
        return token.startswith(f"{user_id}_")

def get_security_utils() -> SecurityUtils:
    """Get security utilities instance"""
    return SecurityUtils()
