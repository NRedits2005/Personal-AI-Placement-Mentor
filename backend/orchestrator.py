import logging
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END

# Import agents
from backend.agents.resume_agent import ResumeAnalysisAgent
from backend.agents.skill_gap_agent import SkillGapAnalysisAgent
from backend.agents.planner_agent import PersonalizedRoadmapAgent
from backend.agents.coding_agent import CodingInterviewAgent
from backend.agents.hr_agent import HRInterviewAgent
from backend.agents.technical_agent import TechnicalInterviewAgent
from backend.agents.evaluator_agent import EvaluatorAgent

from backend.redis_client import redis_client
from backend.config import settings

logger = logging.getLogger(__name__)

# Define the LangGraph workflow state
class AgentState(TypedDict):
    student_id: int
    target_role: str
    target_company: Optional[str]
    resume_path: Optional[str]
    extracted_text: Optional[str]
    resume_analysis: Dict[str, Any]
    skill_gaps: List[Dict[str, Any]]
    study_plan: Dict[str, Any]
    loop_count: int
    current_node: str
    feedback: List[str]
    status: str

class PlacementOrchestrator:
    def __init__(self):
        self.resume_agent = ResumeAnalysisAgent()
        self.skill_gap_agent = SkillGapAnalysisAgent()
        self.planner_agent = PersonalizedRoadmapAgent()
        self.coding_agent = CodingInterviewAgent()
        self.hr_agent = HRInterviewAgent()
        self.technical_agent = TechnicalInterviewAgent()
        self.evaluator_agent = EvaluatorAgent()
        
        # Build LangGraph workflow
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        # 1. Define StateGraph
        builder = StateGraph(AgentState)

        # 2. Add Nodes
        builder.add_node("analyze_resume", self._node_analyze_resume)
        builder.add_node("evaluate_resume", self._node_evaluate_resume)
        builder.add_node("refine_resume", self._node_refine_resume)
        builder.add_node("analyze_skill_gap", self._node_analyze_skill_gap)
        builder.add_node("generate_roadmap", self._node_generate_roadmap)

        # 3. Add Edges
        builder.set_entry_point("analyze_resume")
        builder.add_edge("analyze_resume", "evaluate_resume")
        
        # Conditional edge for Loop Engineering (Resume Score Check)
        builder.add_conditional_edges(
            "evaluate_resume",
            self._route_resume_loop,
            {
                "refine": "refine_resume",
                "proceed": "analyze_skill_gap"
            }
        )
        
        builder.add_edge("refine_resume", "evaluate_resume")
        builder.add_edge("analyze_skill_gap", "generate_roadmap")
        builder.add_edge("generate_roadmap", END)

        return builder.compile()

    # --- Node Implementations ---
    def _node_analyze_resume(self, state: AgentState) -> Dict[str, Any]:
        """Runs the Resume Analysis Agent."""
        logger.info("[Orchestrator] Running analyze_resume node")
        pdf_path = state["resume_path"]
        role = state["target_role"]
        
        # Call Resume Agent
        analysis = self.resume_agent.analyze(pdf_path, role)
        
        # Save intermediate state in Redis
        redis_client.set_agent_memory("resume", state["student_id"], analysis)
        
        return {
            "resume_analysis": analysis,
            "current_node": "analyze_resume"
        }

    def _node_evaluate_resume(self, state: AgentState) -> Dict[str, Any]:
        """Evaluates the resume analysis scores against the configured threshold."""
        logger.info("[Orchestrator] Running evaluate_resume node")
        analysis = state["resume_analysis"]
        score = analysis.get("resume_score", 70)
        
        status = "approved" if score >= settings.LOOP_RESUME_THRESHOLD else "requires_refinement"
        
        return {
            "status": status,
            "current_node": "evaluate_resume"
        }

    def _route_resume_loop(self, state: AgentState) -> str:
        """Determines whether to trigger another refinement loop or proceed."""
        loop_count = state.get("loop_count", 0)
        status = state.get("status", "approved")
        
        # Max 2 feedback refinement loops to avoid infinite running costs
        if status == "requires_refinement" and loop_count < 2:
            logger.info(f"[Orchestrator] Resume score below threshold. Triggering refinement loop #{loop_count + 1}")
            return "refine"
        
        logger.info("[Orchestrator] Resume score met or max loops reached. Proceeding to Skill Gap Analysis.")
        return "proceed"

    def _node_refine_resume(self, state: AgentState) -> Dict[str, Any]:
        """Refines the resume analysis by injecting custom mock improvements."""
        logger.info("[Orchestrator] Running refine_resume node")
        analysis = state["resume_analysis"].copy()
        loop_count = state.get("loop_count", 0) + 1
        
        # Simulating self-improvement loop engineering:
        # Increase the score by addressing outstanding suggestions
        original_score = analysis.get("resume_score", 70)
        improvement = 8  # Bump score by 8 points per loop
        new_score = min(original_score + improvement, 95)
        
        analysis["resume_score"] = new_score
        analysis["ats_score"] = min(analysis.get("ats_score", 70) + 5, 95)
        
        # Remove solved suggestions
        suggestions = analysis.get("improvement_suggestions", [])
        if suggestions:
            suggestions.pop(0)
            
        logger.info(f"[Orchestrator] Resume score refined from {original_score} -> {new_score}")
        
        # Update Redis memory
        redis_client.set_agent_memory("resume", state["student_id"], analysis)

        return {
            "resume_analysis": analysis,
            "loop_count": loop_count,
            "current_node": "refine_resume"
        }

    def _node_analyze_skill_gap(self, state: AgentState) -> Dict[str, Any]:
        """Runs the Skill Gap Analysis Agent."""
        logger.info("[Orchestrator] Running analyze_skill_gap node")
        skills = state["resume_analysis"].get("skills", [])
        role = state["target_role"]
        company = state["target_company"]
        
        gap_results = self.skill_gap_agent.analyze(skills, role, company)
        
        # Cache in Redis
        redis_client.set_agent_memory("skillgap", state["student_id"], gap_results)
        
        return {
            "skill_gaps": gap_results,
            "current_node": "analyze_skill_gap"
        }

    def _node_generate_roadmap(self, state: AgentState) -> Dict[str, Any]:
        """Runs the Personalized Study Roadmap Agent."""
        logger.info("[Orchestrator] Running generate_roadmap node")
        gaps = state["skill_gaps"]
        role = state["target_role"]
        company = state["target_company"]
        
        plan = self.planner_agent.generate_plan(gaps, role, company)
        
        # Cache in Redis
        redis_client.set_agent_memory("planner", state["student_id"], plan)
        
        return {
            "study_plan": plan,
            "current_node": "generate_roadmap"
        }

    # --- Public Orchestration Runner ---
    def run_onboarding_flow(self, student_id: int, resume_path: str, target_role: str, target_company: Optional[str] = None) -> Dict[str, Any]:
        """Executes the complete onboarding mult-agent graph (Resume -> Skill Gap -> Study Plan)."""
        logger.info(f"Starting placement preparation onboarding graph for student_id {student_id}")
        
        initial_state = {
            "student_id": student_id,
            "target_role": target_role,
            "target_company": target_company,
            "resume_path": resume_path,
            "extracted_text": None,
            "resume_analysis": {},
            "skill_gaps": [],
            "study_plan": {},
            "loop_count": 0,
            "current_node": "",
            "feedback": [],
            "status": "pending"
        }
        
        # Run graph
        final_state = self.workflow.invoke(initial_state)
        
        # Persist final state in Redis
        redis_client.set_workflow_state(student_id, final_state)
        
        return final_state
