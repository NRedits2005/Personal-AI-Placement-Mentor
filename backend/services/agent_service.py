import logging
from sqlalchemy.orm import Session
from datetime import datetime

# Import models
from backend.models.resume import Resume
from backend.models.skill_gap import SkillGap
from backend.models.study_plan import StudyPlan
from backend.models.coding_progress import CodingProgress
from backend.models.mock_interview import MockInterview
from backend.models.readiness_score import ReadinessScore
from backend.models.github_project import GitHubProject

# Import orchestrator & agents
from backend.orchestrator import PlacementOrchestrator
from backend.agents.coding_agent import CodingInterviewAgent
from backend.agents.hr_agent import HRInterviewAgent
from backend.agents.technical_agent import TechnicalInterviewAgent
from backend.agents.evaluator_agent import EvaluatorAgent

from backend.redis_client import redis_client

logger = logging.getLogger(__name__)

class AgentService:
    def __init__(self):
        self.orchestrator = PlacementOrchestrator()
        self.coding_agent = CodingInterviewAgent()
        self.hr_agent = HRInterviewAgent()
        self.technical_agent = TechnicalInterviewAgent()
        self.evaluator_agent = EvaluatorAgent()

    def process_resume_onboarding(self, db: Session, student_id: int, file_path: str, target_role: str, target_company: str | None = None) -> dict:
        """Invokes the LangGraph orchestrator and saves the results into PostgreSQL."""
        # 1. Run LangGraph Flow
        result = self.orchestrator.run_onboarding_flow(
            student_id=student_id,
            resume_path=file_path,
            target_role=target_role,
            target_company=target_company
        )
        
        resume_analysis = result["resume_analysis"]
        skill_gaps = result["skill_gaps"]
        study_plan = result["study_plan"]
        
        # 2. Save/Update Resume in DB
        db_resume = db.query(Resume).filter(Resume.student_id == student_id).first()
        if not db_resume:
            db_resume = Resume(student_id=student_id, resume_path=file_path)
            db.add(db_resume)
        
        db_resume.resume_path = file_path
        db_resume.resume_score = resume_analysis.get("resume_score", 0)
        db_resume.ats_score = resume_analysis.get("ats_score", 0)
        db_resume.extracted_skills = resume_analysis.get("skills", [])
        db_resume.github_url = resume_analysis.get("github_url")
        db_resume.linkedin_url = resume_analysis.get("linkedin_url")
        db_resume.improvement_suggestions = resume_analysis.get("improvement_suggestions", [])
        db_resume.created_at = datetime.utcnow()
        
        # 3. Save/Update Skill Gaps
        db_gap = db.query(SkillGap).filter(SkillGap.student_id == student_id).first()
        if not db_gap:
            db_gap = SkillGap(student_id=student_id)
            db.add(db_gap)
        db_gap.skills = skill_gaps
        db_gap.created_at = datetime.utcnow()
        
        # 4. Save/Update Study Plan
        db_plan = db.query(StudyPlan).filter(StudyPlan.student_id == student_id).first()
        if not db_plan:
            db_plan = StudyPlan(student_id=student_id)
            db.add(db_plan)
        db_plan.tasks = study_plan
        db_plan.completion_percentage = 0.0
        db_plan.created_at = datetime.utcnow()
        
        db.commit()
        
        # Recalculate AI Readiness
        self.calculate_readiness_score(db, student_id)
        
        return result

    def get_study_plan(self, db: Session, student_id: int) -> StudyPlan | None:
        return db.query(StudyPlan).filter(StudyPlan.student_id == student_id).first()

    def update_task_progress(self, db: Session, student_id: int, week: str, task_index: int, completed: bool) -> StudyPlan:
        """Updates the completion status of a study task and recalculates the percentage."""
        plan = db.query(StudyPlan).filter(StudyPlan.student_id == student_id).first()
        if not plan:
            raise ValueError("Study plan not found")
            
        tasks = plan.tasks.copy()
        if week in tasks and len(tasks[week]) > task_index:
            tasks[week][task_index]["completed"] = completed
            plan.tasks = tasks
            
            # Recalculate percentage
            total_tasks = 0
            completed_tasks = 0
            for w, task_list in tasks.items():
                for t in task_list:
                    total_tasks += 1
                    if t.get("completed", False):
                        completed_tasks += 1
            
            plan.completion_percentage = (completed_tasks / total_tasks * 100.0) if total_tasks > 0 else 0.0
            db.commit()
            
        return plan

    # --- Interactive Mock Interview Service ---
    def start_mock_interview(self, db: Session, student_id: int, interview_type: str) -> dict:
        """Starts a mock interview session by generating the first question."""
        student = db.query(Resume).filter(Resume.student_id == student_id).first()
        skills = student.extracted_skills if student else []
        github_repos = db.query(GitHubProject).filter(GitHubProject.student_id == student_id).all()
        
        student_profile = {
            "full_name": "Student",
            "target_role": "AI Engineer",
            "target_company": "Google",
            "college": "Placement Prep University",
            "graduation_year": 2026
        }
        
        # Clear existing conversation cache for this category
        redis_key = f"interview_type:{student_id}"
        redis_client.set(redis_key, interview_type)
        redis_client.clear_conversation_history(student_id, category="interview")
        
        # Generate question
        if interview_type == "HR":
            question_data = self.hr_agent.generate_question(student_profile, history=[])
        else:
            repos_data = [{"name": r.repo_name, "description": r.description} for r in github_repos]
            question_data = self.technical_agent.generate_question(
                student_profile,
                resume_summary={"skills": skills},
                github_projects=repos_data,
                history=[]
            )
            
        first_question = question_data.get("question", "Tell me about your tech background.")
        
        # Save question in Redis history
        redis_client.add_conversation_message(
            student_id, 
            {"role": "assistant", "content": first_question}, 
            category="interview"
        )
        
        # Create DB record
        db_interview = MockInterview(
            student_id=student_id,
            interview_type=interview_type,
            questions_answers=[{"question": first_question, "answer": "", "score": 0, "feedback": ""}],
            score=0.0
        )
        db.add(db_interview)
        db.commit()
        
        return {
            "interview_id": db_interview.interview_id,
            "first_question": first_question
        }

    def submit_interview_answer(self, db: Session, student_id: int, interview_id: int, answer: str) -> dict:
        """Saves student response, evaluates, and triggers the next question or finishes interview."""
        interview = db.query(MockInterview).filter(MockInterview.interview_id == interview_id).first()
        if not interview:
            raise ValueError("Interview session not found")
            
        # Get active question (the last one with empty answer)
        q_a_list = list(interview.questions_answers)
        current_qa = next((qa for qa in q_a_list if qa["answer"] == ""), None)
        if not current_qa:
            return {"feedback": "No active question.", "is_complete": True}
            
        current_question = current_qa["question"]
        
        # 1. Run Evaluator Agent
        eval_result = self.evaluator_agent.evaluate_interview_response(
            question=current_question,
            answer=answer,
            context=f"Role: {interview.interview_type}"
        )
        
        # Update current Q&A record
        current_qa["answer"] = answer
        current_qa["score"] = eval_result.get("score", 70)
        current_qa["feedback"] = eval_result.get("feedback", ["Good attempt"])[0] if isinstance(eval_result.get("feedback"), list) else eval_result.get("feedback", "Good attempt")
        
        interview.questions_answers = q_a_list
        db.commit()
        
        # Update Redis conversation history
        redis_client.add_conversation_message(student_id, {"role": "user", "content": answer}, category="interview")
        redis_client.add_conversation_message(student_id, {"role": "assistant", "content": f"Score: {eval_result.get('score')}. Feedback: {current_qa['feedback']}"}, category="interview")
        
        # Check if interview is completed (let's say 3 questions max per mock)
        history = redis_client.get_conversation_history(student_id, category="interview")
        completed_qa_count = sum(1 for qa in q_a_list if qa["answer"] != "")
        
        is_complete = completed_qa_count >= 3
        next_question = None
        
        if not is_complete:
            # Generate next question
            student_profile = {"target_role": "AI Engineer", "target_company": "Google"}
            if interview.interview_type == "HR":
                next_q_data = self.hr_agent.generate_question(student_profile, history=history)
            else:
                student_resume = db.query(Resume).filter(Resume.student_id == student_id).first()
                skills = student_resume.extracted_skills if student_resume else []
                next_q_data = self.technical_agent.generate_question(
                    student_profile,
                    resume_summary={"skills": skills},
                    github_projects=[],
                    history=history
                )
            next_question = next_q_data.get("question", "What are your hobbies?")
            
            # Save next question in DB
            q_a_list.append({"question": next_question, "answer": "", "score": 0, "feedback": ""})
            interview.questions_answers = q_a_list
            db.commit()
            
            # Save in Redis history
            redis_client.add_conversation_message(student_id, {"role": "assistant", "content": next_question}, category="interview")
        else:
            # Compile final score & feedback reports
            scores = [qa.get("score", 0) for qa in q_a_list]
            final_score = sum(scores) / len(scores) if scores else 0.0
            
            interview.score = final_score
            interview.strengths = eval_result.get("strengths", ["Clear speaking"])
            interview.weaknesses = eval_result.get("weaknesses", ["Lacked project details"])
            interview.feedback = eval_result.get("feedback", ["Keep practicing mock runs."])
            db.commit()
            
            # Recalculate AI Readiness
            self.calculate_readiness_score(db, student_id)
            
        return {
            "score": eval_result.get("score", 70),
            "feedback": current_qa["feedback"],
            "next_question": next_question,
            "is_complete": is_complete
        }

    # --- Coding Progress Service ---
    def submit_coding_solution(self, db: Session, student_id: int, question_details: dict, code: str) -> dict:
        """Evaluates DSA code submissions and records student progress."""
        eval_result = self.coding_agent.evaluate_code(question_details, code)
        
        # Fetch or create CodingProgress record
        progress = db.query(CodingProgress).filter(CodingProgress.student_id == student_id).first()
        if not progress:
            progress = CodingProgress(
                student_id=student_id,
                total_solved=0,
                accuracy=0.0,
                weak_topics=[],
                solved_questions=[]
            )
            db.add(progress)
            
        solved = list(progress.solved_questions)
        solved.append({
            "question_id": question_details.get("question_id"),
            "title": question_details.get("title"),
            "score": eval_result.get("score", 0),
            "passed": eval_result.get("passed", False),
            "timestamp": datetime.utcnow().isoformat()
        })
        
        progress.solved_questions = solved
        
        # Calculate new metrics
        passed_count = sum(1 for q in solved if q.get("passed", False))
        progress.total_solved = passed_count
        progress.accuracy = (passed_count / len(solved) * 100.0) if solved else 0.0
        
        # Track weak topics
        weak = list(progress.weak_topics)
        if not eval_result.get("passed", False):
            topic = question_details.get("title")
            if topic not in weak:
                weak.append(topic)
        elif question_details.get("title") in weak:
            weak.remove(question_details.get("title"))
        progress.weak_topics = weak
        
        db.commit()
        
        # Recalculate AI Readiness
        self.calculate_readiness_score(db, student_id)
        
        return eval_result

    # --- AI Readiness Score Analytics ---
    def calculate_readiness_score(self, db: Session, student_id: int) -> ReadinessScore:
        """
        AI Readiness =
        20% Resume +
        25% Coding +
        20% Technical +
        15% HR +
        20% Project
        """
        # 1. Resume Component
        resume = db.query(Resume).filter(Resume.student_id == student_id).first()
        resume_score = resume.resume_score if resume else 0.0
        
        # 2. Coding Component
        coding = db.query(CodingProgress).filter(CodingProgress.student_id == student_id).first()
        coding_score = coding.accuracy if coding else 0.0
        
        # 3. Technical Component
        tech_interviews = db.query(MockInterview).filter(
            MockInterview.student_id == student_id,
            MockInterview.interview_type == "Technical"
        ).all()
        tech_score = sum(i.score for i in tech_interviews) / len(tech_interviews) if tech_interviews else 0.0
        
        # 4. HR Component
        hr_interviews = db.query(MockInterview).filter(
            MockInterview.student_id == student_id,
            MockInterview.interview_type == "HR"
        ).all()
        hr_score = sum(i.score for i in hr_interviews) / len(hr_interviews) if hr_interviews else 0.0
        
        # 5. Project Component (GitHub projects score)
        projects = db.query(GitHubProject).filter(GitHubProject.student_id == student_id).all()
        project_count = len(projects)
        # Base score 50 if they have projects, plus star count weights
        if project_count > 0:
            stars = sum(p.stars for p in projects)
            project_score = min(50 + project_count * 10 + stars * 2, 100)
        else:
            project_score = 0.0
            
        # Overall
        overall = (
            (0.20 * resume_score) +
            (0.25 * coding_score) +
            (0.20 * tech_score) +
            (0.15 * hr_score) +
            (0.20 * project_score)
        )
        
        # Record
        readiness = db.query(ReadinessScore).filter(ReadinessScore.student_id == student_id).order_by(ReadinessScore.created_at.desc()).first()
        # Create a new record each time to capture history
        new_readiness = ReadinessScore(
            student_id=student_id,
            resume_weight_score=resume_score,
            coding_weight_score=coding_score,
            technical_weight_score=tech_score,
            hr_weight_score=hr_score,
            project_weight_score=project_score,
            overall_score=overall
        )
        db.add(new_readiness)
        db.commit()
        db.refresh(new_readiness)
        
        return new_readiness

agent_service = AgentService()
