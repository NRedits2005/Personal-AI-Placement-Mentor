import logging
from datetime import datetime, timedelta
from backend.database import SessionLocal, engine, Base
from backend.utils.hashing import hash_password
from backend.models.student import Student
from backend.models.resume import Resume
from backend.models.skill_gap import SkillGap
from backend.models.study_plan import StudyPlan
from backend.models.coding_progress import CodingProgress
from backend.models.mock_interview import MockInterview
from backend.models.github_project import GitHubProject
from backend.models.readiness_score import ReadinessScore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_data():
    db = SessionLocal()
    try:
        # 1. Clear database
        logger.info("Clearing existing database contents...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        # 2. Seed Test Student
        logger.info("Seeding test student...")
        hashed_pw = hash_password("password123")
        student = Student(
            full_name="Naveen Raj",
            email="test@example.com",
            password_hash=hashed_pw,
            college="AI Engineering Institute of Technology",
            department="Computer Science & Engineering",
            graduation_year=2026,
            target_role="AI Engineer",
            target_company="Google"
        )
        db.add(student)
        db.commit()
        db.refresh(student)

        # 3. Seed Mock Resume
        logger.info("Seeding mock resume analysis...")
        resume = Resume(
            student_id=student.student_id,
            resume_path="./uploads/test_resume.pdf",
            resume_score=85,
            ats_score=88,
            extracted_skills=["Python", "SQL", "Machine Learning", "Git", "Linux"],
            github_url="https://github.com/naveen-raj",
            linkedin_url="https://linkedin.com/in/naveen-raj",
            improvement_suggestions=[
                "Deploy API prototypes in Docker container networks.",
                "Detail system engineering components of recommendation projects."
            ]
        )
        db.add(resume)

        # 4. Seed Mock Skill Gaps
        logger.info("Seeding mock skill gaps...")
        gap = SkillGap(
            student_id=student.student_id,
            skills=[
                {"skill": "Python", "status": "Present", "priority": "Low"},
                {"skill": "SQL", "status": "Present", "priority": "Low"},
                {"skill": "Machine Learning", "status": "Present", "priority": "Medium"},
                {"skill": "FastAPI", "status": "Missing", "priority": "High"},
                {"skill": "Docker", "status": "Missing", "priority": "High"},
                {"skill": "LLMs & RAG", "status": "Missing", "priority": "High"},
                {"skill": "DSA", "status": "Missing", "priority": "Medium"},
                {"skill": "Git", "status": "Present", "priority": "Low"}
            ]
        )
        db.add(gap)

        # 5. Seed Mock Study Roadmap
        logger.info("Seeding mock study roadmap...")
        plan = StudyPlan(
            student_id=student.student_id,
            tasks={
                "Week 1: Core Backend & API Design": [
                    {"task": "Review DSA Arrays & HashMaps", "completed": True},
                    {"task": "Build CRUD API with FastAPI", "completed": False},
                    {"task": "Implement SQL Joins & Index optimization", "completed": True}
                ],
                "Week 2: Devops & System Design": [
                    {"task": "Dockerize the FastAPI Application", "completed": False},
                    {"task": "Understand Docker Compose environment networks", "completed": False},
                    {"task": "Learn basic Git branching workflows", "completed": True}
                ],
                "Week 3: Advanced AI & RAG Deployment": [
                    {"task": "Integrate OpenAI API with FastAPI", "completed": False},
                    {"task": "Build a Simple RAG application with ChromaDB", "completed": False},
                    {"task": "Deploy app locally with Docker-Compose", "completed": False}
                ]
            },
            completion_percentage=33.3
        )
        db.add(plan)

        # 6. Seed Mock GitHub Repos
        logger.info("Seeding mock GitHub projects...")
        repo1 = GitHubProject(
            student_id=student.student_id,
            repo_name="Customer-Loyalty-Recommendation-System",
            repo_url="https://github.com/naveen-raj/Customer-Loyalty-Recommendation-System",
            description="Collaborative filtering recommendation engine with role-based access control and scalability layers using Streamlit and PostgreSQL.",
            languages={"Python": 92.5, "SQL": 7.5},
            stars=12,
            metadata_info={}
        )
        repo2 = GitHubProject(
            student_id=student.student_id,
            repo_name="Distributed-Key-Value-Store",
            repo_url="https://github.com/naveen-raj/Distributed-Key-Value-Store",
            description="Consistent hashing and raft consensus protocol implementation in Go.",
            languages={"Go": 100.0},
            stars=18,
            metadata_info={}
        )
        db.add(repo1)
        db.add(repo2)

        # 7. Seed Mock Interviews
        logger.info("Seeding mock interview histories...")
        hr_mock = MockInterview(
            student_id=student.student_id,
            interview_type="HR",
            questions_answers=[
                {
                    "question": "Tell me about yourself.",
                    "answer": "I am a computer science student specializing in AI systems. I build predictive recommenders.",
                    "score": 85,
                    "feedback": "Clear explanation of specialties. Add details about college achievements."
                },
                {
                    "question": "Describe a conflict in a project.",
                    "answer": "We disagreed on using Streamlit vs React. I showed data proving Streamlit was faster to code.",
                    "score": 80,
                    "feedback": "Good application of data-driven conflict resolution. Outline teammate feelings."
                }
            ],
            score=82.5,
            strengths=["Concise speech", "Logical structural outline"],
            weaknesses=["Lacked details on target team coordination metrics"],
            feedback=["Incorporate the STAR methodology to state background context."]
        )
        tech_mock = MockInterview(
            student_id=student.student_id,
            interview_type="Technical",
            questions_answers=[
                {
                    "question": "How do you handle Cold Start for new users in your loyalty recommendation system?",
                    "answer": "We fall back to popularity-based recommendations or prompt the user for initial interest tags.",
                    "score": 90,
                    "feedback": "Perfect! Shows excellent system engineering trade-off understanding."
                },
                {
                    "question": "Explain consistency hashing in distributed key-value stores.",
                    "answer": "It distributes keys across nodes arranged in a hash ring. Adding nodes only remaps a fraction of keys.",
                    "score": 88,
                    "feedback": "Accurate rings and virtual nodes remapping explanation."
                }
            ],
            score=89.0,
            strengths=["Superb database scalability insights", "Accurate algorithm details"],
            weaknesses=["Missed re-replication logic details during hash ring node failover"],
            feedback=["Explain node replica tracking concepts during ring failures."]
        )
        db.add(hr_mock)
        db.add(tech_mock)

        # 8. Seed Coding Progress
        logger.info("Seeding mock coding progress...")
        progress = CodingProgress(
            student_id=student.student_id,
            total_solved=4,
            accuracy=80.0,
            weak_topics=["Dynamic Programming"],
            solved_questions=[
                {"question_id": "two_sum", "title": "Two Sum", "score": 100, "passed": True, "timestamp": datetime.utcnow().isoformat()},
                {"question_id": "reverse_linked_list", "title": "Reverse Linked List", "score": 100, "passed": True, "timestamp": datetime.utcnow().isoformat()},
                {"question_id": "longest_substring", "title": "Longest Substring", "score": 90, "passed": True, "timestamp": datetime.utcnow().isoformat()},
                {"question_id": "coin_change", "title": "Coin Change (DP)", "score": 50, "passed": False, "timestamp": datetime.utcnow().isoformat()}
            ]
        )
        db.add(progress)
        db.commit()

        # 9. Calculate Readiness Score
        logger.info("Calculating initial AI Readiness score history...")
        # Overall readiness score = 20% Resume (85) + 25% Coding (80) + 20% Technical Mock (89) + 15% HR Mock (82.5) + 20% Project (50 + 2 * 10 + 30 stars = 100)
        # = 17 + 20 + 17.8 + 12.375 + 20 = 87.175
        r_hist1 = ReadinessScore(
            student_id=student.student_id,
            resume_weight_score=80.0,
            coding_weight_score=60.0,
            technical_weight_score=75.0,
            hr_weight_score=70.0,
            project_weight_score=60.0,
            overall_score=68.5,
            created_at=datetime.utcnow() - timedelta(days=2)
        )
        r_hist2 = ReadinessScore(
            student_id=student.student_id,
            resume_weight_score=85.0,
            coding_weight_score=80.0,
            technical_weight_score=89.0,
            hr_weight_score=82.5,
            project_weight_score=100.0,
            overall_score=87.2,
            created_at=datetime.utcnow()
        )
        db.add(r_hist1)
        db.add(r_hist2)
        db.commit()

        logger.info("Database successfully seeded with placement metrics.")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
