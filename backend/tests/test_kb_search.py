"""Tests for knowledge base search tool"""
import pytest
from app.agent.tools.kb_search import KnowledgeBaseSearchTool


class TestKnowledgeBaseSearchTool:
    """Tests for the KnowledgeBaseSearchTool class"""

    def setup_method(self):
        self.tool = KnowledgeBaseSearchTool()

    def test_wifi_search(self):
        """Test searching for Wi-Fi issues"""
        query = "wifi keeps disconnecting on iPhone"
        result = self.tool._run(query=query, top_k=3)

        assert "query" in result
        assert result["query"] == query
        assert "results_found" in result
        assert result["results_found"] > 0
        assert "results" in result
        assert isinstance(result["results"], list)

    def test_battery_search(self):
        """Test searching for battery issues"""
        query = "battery drains quickly"
        result = self.tool._run(query=query, top_k=2)

        assert result["results_found"] >= 0
        assert isinstance(result["results"], list)

    def test_storage_search(self):
        """Test searching for storage issues"""
        query = "low storage warning"
        result = self.tool._run(query=query)

        assert result["results_found"] >= 0
        assert len(result["results"]) <= 5

    def test_search_with_top_k(self):
        """Test limiting number of results"""
        query = "network troubleshooting"
        result = self.tool._run(query=query, top_k=1)

        assert len(result["results"]) <= 1

    def test_async_search(self):
        """Test async version of search"""
        import asyncio

        async def run_async():
            return await self.tool._arun(query="battery issues", top_k=2)

        result = asyncio.run(run_async())
        assert "results" in result
