"""Tests for agent orchestrator"""
import pytest
from unittest.mock import patch, MagicMock
from app.agent.orchestrator import TechSupportAgentOrchestrator
from app.agent.state import AgentState, ConversationMessage


class TestTechSupportAgentOrchestrator:
    """Tests for the TechSupportAgentOrchestrator class"""

    @pytest.fixture
    def orchestrator(self):
        return TechSupportAgentOrchestrator(anthropic_api_key="test-key")

    def test_intake_issue_classification(self, orchestrator):
        """Test that user messages are correctly classified"""
        state: AgentState = {
            "messages": [
                ConversationMessage(
                    role="user",
                    content="My Wi-Fi keeps disconnecting"
                )
            ],
            "user_id": "test-user",
            "session_id": "test-session",
            "device_telemetry": None,
            "screenshot_analysis": None,
            "kb_search_results": None,
            "tool_executions": [],
            "current_hypothesis": None,
            "recommended_actions": [],
            "requires_hitl_approval": False,
            "next_step": "collect_telemetry"
        }

        result = orchestrator._intake_issue(state)
        assert result["next_step"] == "collect_telemetry"

    def test_intake_storage_issue_classification(self, orchestrator):
        """Test storage issue classification"""
        state: AgentState = {
            "messages": [
                ConversationMessage(
                    role="user",
                    content="My phone says storage is low"
                )
            ],
            "user_id": "test-user",
            "session_id": "test-session",
            "device_telemetry": None,
            "screenshot_analysis": None,
            "kb_search_results": None,
            "tool_executions": [],
            "current_hypothesis": None,
            "recommended_actions": [],
            "requires_hitl_approval": False,
            "next_step": "collect_telemetry"
        }

        result = orchestrator._intake_issue(state)
        assert result["next_step"] == "collect_telemetry"

    def test_intake_screenshot_classification(self, orchestrator):
        """Test screenshot/request for image classification"""
        state: AgentState = {
            "messages": [
                ConversationMessage(
                    role="user",
                    content="Here is the screenshot of the error"
                )
            ],
            "user_id": "test-user",
            "session_id": "test-session",
            "device_telemetry": None,
            "screenshot_analysis": None,
            "kb_search_results": None,
            "tool_executions": [],
            "current_hypothesis": None,
            "recommended_actions": [],
            "requires_hitl_approval": False,
            "next_step": "collect_telemetry"
        }

        result = orchestrator._intake_issue(state)
        # Screenshot-related should still check telemetry first
        assert result["next_step"] in ["collect_telemetry", "search_kb"]

    def test_collect_telemetry_adds_analysis(self, orchestrator):
        """Test that telemetry collection adds analysis to state"""
        state: AgentState = {
            "messages": [],
            "user_id": "test-user",
            "session_id": "test-session",
            "device_telemetry": MagicMock(),
            "screenshot_analysis": None,
            "kb_search_results": None,
            "tool_executions": [],
            "current_hypothesis": None,
            "recommended_actions": [],
            "requires_hitl_approval": False,
            "next_step": "collect_telemetry"
        }

        result = orchestrator._collect_telemetry(state)
        assert len(result["tool_executions"]) > 0

    def test_route_after_intake(self, orchestrator):
        """Test the route function after intake"""
        state: AgentState = {
            "messages": [],
            "user_id": "test-user",
            "session_id": "test-session",
            "device_telemetry": None,
            "screenshot_analysis": None,
            "kb_search_results": None,
            "tool_executions": [],
            "current_hypothesis": None,
            "recommended_actions": [],
            "requires_hitl_approval": False,
            "next_step": "search_kb"
        }

        result = orchestrator._route_after_intake(state)
        assert result == "search_kb"

    def test_check_hitl_required(self, orchestrator):
        """Test HITL approval check"""
        state: AgentState = {
            "messages": [],
            "user_id": "test-user",
            "session_id": "test-session",
            "device_telemetry": None,
            "screenshot_analysis": None,
            "kb_search_results": None,
            "tool_executions": [],
            "current_hypothesis": None,
            "recommended_actions": [],
            "requires_hitl_approval": True,
            "next_step": "end"
        }

        result = orchestrator._check_hitl_required(state)
        assert result == "hitl"

    def test_check_hitl_not_required(self, orchestrator):
        """Test when HITL is not required"""
        state: AgentState = {
            "messages": [],
            "user_id": "test-user",
            "session_id": "test-session",
            "device_telemetry": None,
            "screenshot_analysis": None,
            "kb_search_results": None,
            "tool_executions": [],
            "current_hypothesis": None,
            "recommended_actions": [],
            "requires_hitl_approval": False,
            "next_step": "end"
        }

        result = orchestrator._check_hitl_required(state)
        assert result == "end"

    def test_search_kb_adds_results(self, orchestrator):
        """Test that KB search adds results"""
        state: AgentState = {
            "messages": [
                ConversationMessage(
                    role="user",
                    content="Wi-Fi issues"
                )
            ],
            "user_id": "test-user",
            "session_id": "test-session",
            "device_telemetry": None,
            "screenshot_analysis": None,
            "kb_search_results": None,
            "tool_executions": [],
            "current_hypothesis": None,
            "recommended_actions": [],
            "requires_hitl_approval": False,
            "next_step": "search_kb"
        }

        result = orchestrator._search_kb(state)
        assert "kb_search_results" in result
        assert result["kb_search_results"] is not None
