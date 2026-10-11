# Agent Orchestrator - LangGraph State Machine
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from datetime import datetime
import logging

from app.agent.state import AgentState, ConversationMessage, ToolExecution
from app.agent.tools import (
    DeviceTelemetryTool,
    NetworkDiagnosticsTool,
    KnowledgeBaseSearchTool,
    ScreenshotAnalyzerTool,
    DeepLinkGeneratorTool,
)

logger = logging.getLogger(__name__)

class TechSupportAgentOrchestrator:
    def __init__(self, anthropic_api_key: str):
        self.device_telemetry_tool = DeviceTelemetryTool()
        self.network_diagnostics_tool = NetworkDiagnosticsTool()
        self.kb_search_tool = KnowledgeBaseSearchTool()
        self.screenshot_analyzer_tool = ScreenshotAnalyzerTool()
        self.deep_link_generator_tool = DeepLinkGeneratorTool()

        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(AgentState)

        workflow.add_node("intake", self._intake_issue)
        workflow.add_node("collect_telemetry", self._collect_telemetry)
        workflow.add_node("analyze_network", self._analyze_network)
        workflow.add_node("search_kb", self._search_kb)
        workflow.add_node("analyze_screenshot", self._analyze_screenshot)
        workflow.add_node("generate_solution", self._generate_solution)
        workflow.add_node("hitl_checkpoint", self._hitl_checkpoint)

        workflow.set_entry_point("intake")

        workflow.add_conditional_edges(
            "intake",
            self._route_after_intake,
            {
                "collect_telemetry": "collect_telemetry",
                "search_kb": "search_kb",
                "analyze_screenshot": "analyze_screenshot",
                "generate_solution": "generate_solution",
            }
        )

        workflow.add_edge("collect_telemetry", "analyze_network")
        workflow.add_edge("analyze_network", "search_kb")
        workflow.add_edge("analyze_screenshot", "search_kb")
        workflow.add_edge("search_kb", "generate_solution")

        workflow.add_conditional_edges(
            "generate_solution",
            self._check_hitl_required,
            {
                "hitl": "hitl_checkpoint",
                "end": END
            }
        )

        workflow.add_edge("hitl_checkpoint", END)

        return workflow.compile()

    def _intake_issue(self, state: AgentState) -> AgentState:
        """Analyze initial user message and determine diagnostic path"""
        user_message = next(
            (msg for msg in reversed(state["messages"]) if msg.role == "user"),
            None
        )

        if not user_message:
            state["next_step"] = "end"
            return state

        # Determine next step based on message content
        query_lower = user_message.content.lower()
        state["next_step"] = "search_kb"

        if any(kw in query_lower for kw in ["wifi", "internet", "network", "connect"]):
            state["next_step"] = "collect_telemetry"
        elif any(kw in query_lower for kw in ["battery", "charge", "power"]):
            state["next_step"] = "collect_telemetry"
        elif any(kw in query_lower for kw in ["storage", "space", "memory"]):
            state["next_step"] = "collect_telemetry"
        elif any(kw in query_lower for kw in ["screenshot", "picture", "image", "show"]):
            state["next_step"] = "analyze_screenshot"
        elif any(kw in query_lower for kw in ["error", "bug", "issue", "problem"]):
            state["next_step"] = "search_kb"

        state["current_hypothesis"] = f"Initial assessment: {state['next_step']}"
        return state

    def _route_after_intake(self, state: AgentState) -> str:
        return state.get("next_step", "generate_solution")

    def _collect_telemetry(self, state: AgentState) -> AgentState:
        if not state.get("device_telemetry"):
            state["messages"].append(ConversationMessage(
                role="assistant",
                content="[SYSTEM: REQUEST_TELEMETRY]",
                metadata={"action": "request_telemetry"}
            ))
            return state

        analysis = self.device_telemetry_tool._run(
            telemetry_data=state["device_telemetry"].dict()
        )

        state["tool_executions"].append(ToolExecution(
            tool_name="analyze_device_telemetry",
            input_params={"telemetry": "provided"},
            output=analysis,
            success=True
        ))

        if analysis["issues"]:
            issues_summary = ", ".join([i["type"] for i in analysis["issues"]])
            state["current_hypothesis"] = f"Detected issues: {issues_summary}"

        return state

    def _analyze_network(self, state: AgentState) -> AgentState:
        if not state.get("device_telemetry"):
            return state

        analysis = self.network_diagnostics_tool._run(
            telemetry_data=state["device_telemetry"].dict()
        )

        state["tool_executions"].append(ToolExecution(
            tool_name="analyze_network_diagnostics",
            input_params={},
            output=analysis,
            success=True
        ))

        return state

    def _search_kb(self, state: AgentState) -> AgentState:
        user_message = next(
            (msg for msg in reversed(state["messages"]) if msg.role == "user"),
            None
        )
        query = user_message.content if user_message else "general troubleshooting"

        kb_analysis = next(
            (t.output for t in state["tool_executions"]
             if t.tool_name == "analyze_device_telemetry"),
            None
        )

        if kb_analysis and kb_analysis.get("issues"):
            issue_types = [i["type"] for i in kb_analysis["issues"]]
            query += f" {' '.join(issue_types)}"

        results = self.kb_search_tool._run(query=query, top_k=3)

        state["kb_search_results"] = results["results"]
        state["tool_executions"].append(ToolExecution(
            tool_name="search_tech_support_kb",
            input_params={"query": query},
            output=results,
            success=True
        ))

        return state

    def _analyze_screenshot(self, state: AgentState) -> AgentState:
        screenshot_msg = next(
            (msg for msg in reversed(state["messages"])
             if msg.metadata and msg.metadata.get("screenshot")),
            None
        )

        if not screenshot_msg:
            state["messages"].append(ConversationMessage(
                role="assistant",
                content="Could you share a screenshot of the issue? This will help me diagnose it better.",
                metadata={"action": "request_screenshot"}
            ))
            return state

        analysis = self.screenshot_analyzer_tool._run(
            image_base64=screenshot_msg.metadata["screenshot"],
            user_description=screenshot_msg.content
        )

        state["screenshot_analysis"] = analysis
        state["tool_executions"].append(ToolExecution(
            tool_name="analyze_screenshot",
            input_params={"has_screenshot": True},
            output=analysis,
            success=True
        ))

        return state

    def _generate_solution(self, state: AgentState) -> AgentState:
        context = {
            "user_issue": state["messages"][0].content if state["messages"] else "",
            "telemetry_issues": None,
            "kb_articles": state.get("kb_search_results", []),
            "screenshot_findings": state.get("screenshot_analysis"),
        }

        telemetry_exec = next(
            (t for t in state["tool_executions"]
             if t.tool_name == "analyze_device_telemetry"),
            None
        )
        if telemetry_exec:
            context["telemetry_issues"] = telemetry_exec.output.get("issues", [])

        # Generate deep link actions based on detected issues
        deep_link_actions = []
        if context["telemetry_issues"]:
            for issue in context["telemetry_issues"]:
                action = self._map_issue_to_deep_link(issue["type"])
                if action:
                    deep_link_actions.append(action)

        state["recommended_actions"] = deep_link_actions
        state["requires_hitl_approval"] = any(
            i["severity"] == "high" for i in (context["telemetry_issues"] or [])
        )

        # Create solution message
        explanation = self._generate_explanation(context)
        state["messages"].append(ConversationMessage(
            role="assistant",
            content=explanation,
            metadata={"actions": deep_link_actions}
        ))

        return state

    def _map_issue_to_deep_link(self, issue_type: str) -> Dict[str, Any] | None:
        platform_map = {
            "wifi": {"type": "wifi", "label": "Wi-Fi Settings", "description": "Open Wi-Fi settings"},
            "storage": {"type": "storage", "label": "Storage Management", "description": "Free up storage space"},
            "battery": {"type": "battery", "label": "Battery Settings", "description": "Check battery usage"},
        }
        return platform_map.get(issue_type)

    def _generate_explanation(self, context: Dict[str, Any]) -> str:
        if context["kb_articles"]:
            article = context["kb_articles"][0]
            return f"Based on my analysis, this appears to be related to: {article['title']}. \n\n" \
                   f"Recommended steps:\n" \
                   f"1. Review the troubleshooting steps for this issue\n" \
                   f"2. Try opening the relevant settings to verify your configuration"
        return "I've analyzed your device and found some potential issues. Let me know if you'd like me to suggest specific solutions."

    def _check_hitl_required(self, state: AgentState) -> str:
        return "hitl" if state.get("requires_hitl_approval") else "end"

    def _hitl_checkpoint(self, state: AgentState) -> AgentState:
        state["messages"].append(ConversationMessage(
            role="assistant",
            content="[SYSTEM: HITL_APPROVAL_REQUIRED]",
            metadata={
                "action": "request_approval",
                "actions": state["recommended_actions"]
            }
        ))
        return state

    async def run(self, initial_state: AgentState) -> AgentState:
        try:
            final_state = await self.graph.ainvoke(initial_state)
            return final_state
        except Exception as e:
            logger.error(f"Agent execution error: {e}")
            raise
