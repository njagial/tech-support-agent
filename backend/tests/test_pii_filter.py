"""Tests for PII filter service"""
import pytest
from app.services.pii_filter import PIIFilter


class TestPIIFilter:
    """Tests for the PIIFilter class"""

    @pytest.fixture
    def filter(self):
        return PIIFilter()

    def test_email_detection(self, filter):
        """Test email detection"""
        text = "Contact me at john.doe@example.com for help"
        result = filter.detect_pii(text)

        assert result["has_pii"] == True
        assert "email" in result["pii_types"]

    def test_phone_detection(self, filter):
        """Test phone number detection"""
        text = "Call me at 555-123-4567"
        result = filter.detect_pii(text)

        assert result["has_pii"] == True
        assert "phone" in result["pii_types"]

    def test_ssn_detection(self, filter):
        """Test SSN detection"""
        text = "My SSN is 123-45-6789"
        result = filter.detect_pii(text)

        assert result["has_pii"] == True
        assert "ssn" in result["pii_types"]

    def test_credit_card_detection(self, filter):
        """Test credit card detection"""
        text = "Card number: 1234-5678-9012-3456"
        result = filter.detect_pii(text)

        assert result["has_pii"] == True
        assert "credit_card" in result["pii_types"]

    def test_password_detection(self, filter):
        """Test password detection"""
        text = "password: mysecretpassword123"
        result = filter.detect_pii(text)

        assert result["has_pii"] == True
        assert "password" in result["pii_types"]

    def test_no_pii_detection(self, filter):
        """Test text without PII"""
        text = "Hello, this is a normal text without any sensitive information"
        result = filter.detect_pii(text)

        assert result["has_pii"] == False
        assert len(result["pii_types"]) == 0

    def test_text_redaction(self, filter):
        """Test PII redaction from text"""
        text = "Email: john@example.com, Phone: 555-123-4567"
        result = filter.redact_text(text)

        assert "john@example.com" not in result
        assert "555-123-4567" not in result
        assert "[REDACTED]" in result

    def test_multiple_pii_redaction(self, filter):
        """Test redaction of multiple PII types"""
        text = "Email: test@company.com and password: secret123"
        result = filter.redact_text(text)

        assert "[REDACTED]" in result
        assert "test@company.com" not in result
        assert "secret123" not in result

    def test_hash_user_id(self, filter):
        """Test user ID hashing"""
        user_id = "user-12345"
        hash_result = filter.hash_user_id(user_id)

        assert len(hash_result) == 16
        assert hash_result != user_id

    def test_filter_screenshot_content(self, filter):
        """Test filtering screenshot OCR content"""
        ocr_text = "Error code: 123 Contact support@example.com"

        result = filter.filter_screenshot_content(ocr_text)

        assert result["detected"] == True
        assert "email" in result["pii_types"]
        assert result["should_redact"] == True
        assert "REDACTED" in result["redacted_text"]
