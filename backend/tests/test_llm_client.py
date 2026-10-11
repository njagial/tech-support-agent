"""Tests for LLM client"""
import pytest
from unittest.mock import MagicMock, patch
from app.services.llm_client import LLMClient


class TestLLMClient:
    """Tests for the LLMClient class"""

    @pytest.fixture
    def client(self):
        return LLMClient(api_key="test-key")

    def test_initialization(self, client):
        """Test client initialization"""
        assert client.primary_model == "claude-3-5-sonnet-20241022"
        assert client.fast_model == "claude-3-5-haiku-20241022"

    @pytest.mark.asyncio
    async def test_generate_text_with_mock(self, client):
        """Test text generation with mocked API"""
        with patch.object(client.client.messages, 'create') as mock_create:
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text="Test response")]
            mock_create.return_value = mock_response

            result = await client.generate_text("Test prompt")

            assert "Test response" in result
            mock_create.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_text_fallback(self, client):
        """Test fallback to fast model on rate limit"""
        with patch.object(client.client.messages, 'create') as mock_create:
            from anthropic import RateLimitError

            # First call raises rate limit, second succeeds
            def side_effect(*args, **kwargs):
                if mock_create.call_count == 1:
                    raise RateLimitError("Rate limited")
                mock_response = MagicMock()
                mock_response.content = [MagicMock(text="Fallback response")]
                return mock_response

            mock_create.side_effect = side_effect

            result = await client.generate_text("Test prompt")

            assert "Fallback response" in result

    @pytest.mark.asyncio
    async def test_analyze_image(self, client):
        """Test image analysis"""
        test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

        with patch.object(client.client.messages, 'create') as mock_create:
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text="Image analysis result")]
            mock_create.return_value = mock_response

            result = await client.analyze_image(test_image, "Analyze this image")

            assert result["success"] == True
            assert "analysis" in result

    @pytest.mark.asyncio
    async def test_classify_intent(self, client):
        """Test intent classification"""
        with patch.object(client, 'generate_text') as mock_generate:
            mock_generate.return_value = "category: network\nconfidence: 0.9"

            result = await client.classify_intent(
                "My Wi-Fi is not working",
                ["network", "battery", "storage"]
            )

            assert "user_message" in result
            assert "response" in result
