# Knowledge Base Search Tool
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class KBSearchInput(BaseModel):
    query: str = Field(description="Natural language query describing the technical issue")
    top_k: int = Field(default=5, description="Number of results to return")

class KnowledgeBaseSearchTool(BaseTool):
    name: str = "search_tech_support_kb"
    description: str = """
    Search the technical support knowledge base for relevant solutions.
    Input: Natural language description of the issue.
    Returns: List of relevant KB articles with troubleshooting steps.
    """
    args_schema: type[BaseModel] = KBSearchInput

    def _run(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Synchronous KB search - using mock data in development"""
        # In production, this would query Qdrant vector store
        mock_results = [
            {
                "title": "Wi-Fi Connection Issues",
                "content": "If your device keeps disconnecting from Wi-Fi, try the following steps: 1) Forget the network and reconnect, 2) Check if Airplane mode is off, 3) Restart your router, 4) Update your device's software",
                "source": "iOS Support KB",
                "relevance_score": 0.89,
                "os": "ios",
                "issue_category": "network"
            },
            {
                "title": "Low Storage Warning",
                "content": "When storage is low, delete unused apps, photos, or videos. Go to Settings > General > Storage to manage your space.",
                "source": "Mobile Device Guide",
                "relevance_score": 0.85,
                "os": "both",
                "issue_category": "storage"
            }
        ]

        return {
            "query": query,
            "results_found": len(mock_results),
            "results": mock_results
        }

    async def _arun(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        return self._run(query, top_k)
