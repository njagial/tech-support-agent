# Knowledge Base Search Tool
from typing import Dict, Any, List


class KnowledgeBaseSearchTool:
    """Search the technical support knowledge base for relevant solutions"""

    def search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Synchronous KB search - using mock data"""
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
            "results": mock_results[:top_k]
        }

    async def search_async(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Async version"""
        return self.search(query, top_k)
