# LLM Client - Anthropic Integration
from anthropic import Anthropic, APIError, RateLimitError
from typing import Dict, Any, Optional
import logging
import functools

logger = logging.getLogger(__name__)

def retry_on_rate_limit(max_retries=3, delay_seconds=2):
    """Retry decorator for rate limit handling"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except RateLimitError:
                    if attempt == max_retries - 1:
                        raise
                    import asyncio
                    await asyncio.sleep(delay_seconds * (attempt + 1))
            return None
        return wrapper
    return decorator

class LLMClient:
    def __init__(self, api_key: str, primary_model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic(api_key=api_key)
        self.primary_model = primary_model
        self.fast_model = "claude-3-5-haiku-20241022"

    @retry_on_rate_limit(max_retries=3)
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        use_fast_model: bool = False
    ) -> str:
        """Generate text response from LLM"""
        try:
            response = self.client.messages.create(
                model=self.primary_model if not use_fast_model else self.fast_model,
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                system=system_prompt
            )
            return response.content[0].text
        except RateLimitError:
            # Fallback to faster model
            logger.warning("Rate limited, falling back to Haiku")
            response = self.client.messages.create(
                model=self.fast_model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except APIError as e:
            logger.error(f"Anthropic API error: {e}")
            return f"Error: {str(e)}"

    async def analyze_image(
        self,
        image_base64: str,
        prompt: str,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """Analyze image using Claude Vision"""
        try:
            response = self.client.messages.create(
                model=self.primary_model,
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_base64
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }]
            )
            return {"analysis": response.content[0].text, "success": True}
        except APIError as e:
            logger.error(f"Image analysis error: {e}")
            return {"analysis": None, "error": str(e)}

    async def classify_intent(
        self,
        user_message: str,
        categories: list[str]
    ) -> Dict[str, Any]:
        """Classify user message intent using structured output"""
        prompt = f"""Classify the user's request into one of these categories: {', '.join(categories)}

User message: "{user_message}"

Return JSON with: category, confidence (0-1), and reasoning."""

        response = await self.generate_text(prompt, max_tokens=500, use_fast_model=True)
        return {"user_message": user_message, "response": response}
