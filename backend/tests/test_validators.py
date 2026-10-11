"""Tests for validators"""
import pytest
from app.utils.validators import Validators, validate_chat_request


class TestValidators:
    """Tests for the Validators class"""

    def test_valid_email(self):
        """Test valid email addresses"""
        assert Validators.is_valid_email("test@example.com") == True
        assert Validators.is_valid_email("user.name@domain.co.uk") == True
        assert Validators.is_valid_email("test123@test.io") == True

    def test_invalid_email(self):
        """Test invalid email addresses"""
        assert Validators.is_valid_email("invalid") == False
        assert Validators.is_valid_email("@example.com") == False
        assert Validators.is_valid_email("test@") == False

    def test_valid_phone(self):
        """Test valid phone numbers"""
        assert Validators.is_valid_phone("5551234567") == True
        assert Validators.is_valid_phone("+1-555-123-4567") == True
        assert Validators.is_valid_phone("555-123-4567") == True

    def test_invalid_phone(self):
        """Test invalid phone numbers"""
        assert Validators.is_valid_phone("123") == False
        assert Validators.is_valid_phone("abc-def-ghij") == False

    def test_sanitize_text(self):
        """Test text sanitization"""
        text = "<script>alert('xss')</script> Hello & welcome!"
        result = Validators.sanitize_text(text)

        assert "<" not in result
        assert ">" not in result
        assert "&" not in result
        assert "Hello" in result

    def test_validate_image_base64_valid(self):
        """Test valid base64 image data"""
        valid_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        assert Validators.validate_image_base64(valid_base64) == True

    def test_validate_image_base64_invalid(self):
        """Test invalid base64 image data"""
        assert Validators.validate_image_base64("") == False
        assert Validators.validate_image_base64("not base64") == False
        assert Validators.validate_image_base64(None) == False

    def test_validate_telemetry_valid(self):
        """Test valid telemetry data"""
        telemetry = {
            "device": {"model": "Test"},
            "battery": {"level": 0.5},
            "storage": {"usedPercentage": 50},
            "network": {"isConnected": True},
            "timestamp": "2024-01-01T00:00:00"
        }
        assert Validators.validate_telemetry(telemetry) == True

    def test_validate_telemetry_missing_fields(self):
        """Test telemetry data with missing fields"""
        telemetry = {"device": {"model": "Test"}}
        assert Validators.validate_telemetry(telemetry) == False

    def test_size_limit_check(self):
        """Test file size validation"""
        small_text = "a" * 100
        assert Validators.is_within_size_limit(small_text, max_mb=5) == True

        large_text = "a" * (6 * 1024 * 1024)  # 6MB
        assert Validators.is_within_size_limit(large_text, max_mb=5) == False


class TestValidateChatRequest:
    """Tests for the validate_chat_request function"""

    def test_valid_chat_request(self):
        """Test valid chat request"""
        data = {"message": "Hello", "user_id": "user123"}
        valid, error = validate_chat_request(data)

        assert valid == True
        assert error == ""

    def test_missing_message(self):
        """Test missing message"""
        data = {"user_id": "user123"}
        valid, error = validate_chat_request(data)

        assert valid == False
        assert "Message is required" in error

    def test_missing_user_id(self):
        """Test missing user_id"""
        data = {"message": "Hello"}
        valid, error = validate_chat_request(data)

        assert valid == False
        assert "User ID is required" in error

    def test_message_too_long(self):
        """Test message too long"""
        data = {"message": "a" * 5001, "user_id": "user123"}
        valid, error = validate_chat_request(data)

        assert valid == False
        assert "too long" in error
