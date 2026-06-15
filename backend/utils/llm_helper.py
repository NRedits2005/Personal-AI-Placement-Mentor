import os
import json
import logging
import re
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from backend.config import settings

logger = logging.getLogger(__name__)

def get_llm():
    api_key = settings.OPENAI_API_KEY
    if not api_key or api_key in ["mock-or-real-api-key", "your_openai_api_key_here", ""]:
        return None
    try:
        kwargs = {
            "model_name": settings.LLM_MODEL,
            "openai_api_key": api_key,
            "temperature": 0.2
        }
        if settings.LLM_BASE_URL:
            kwargs["openai_api_base"] = settings.LLM_BASE_URL
        return ChatOpenAI(**kwargs)
    except Exception as e:
        logger.warning(f"Error initializing ChatOpenAI: {e}. Falling back to mock responses.")
        return None

def call_llm(prompt: str, system_prompt: str = "You are a senior AI career mentor.", response_format: str = "json") -> str:
    """Invokes LLM or returns high-quality mock responses if LLM is unavailable."""
    llm = get_llm()
    if llm:
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=prompt)
            ]
            response = llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM execution failed: {e}. Routing to mock fallback.")

    # Return mock response matching requested schema
    return get_mock_response(prompt, response_format)

def get_mock_response(prompt: str, response_format: str) -> str:
    """Generates mock JSON/Text answers depending on prompt keywords."""
    p_lower = prompt.lower()
    
    # 1. Resume analysis
    if "ats" in p_lower or "resume_score" in p_lower:
        return json.dumps({
            "resume_score": 82,
            "ats_score": 86,
            "skills": ["Python", "SQL", "Machine Learning", "Git", "Linux"],
            "missing_sections": ["GitHub Link", "Professional Summary"],
            "improvement_suggestions": [
                "Include your GitHub link under contact information to showcase repository contributions.",
                "Add a professional summary highlighting your target role as an AI Engineer.",
                "Detail your project architectures (e.g. mention FastAPI and Docker in project summaries)."
            ]
        }, indent=2)

    # 2. Skill Gap Analysis
    elif "skill gap" in p_lower or "target_role" in p_lower:
        # Check target role
        role = "AI Engineer"
        if "frontend" in p_lower or "react" in p_lower:
            role = "Frontend Engineer"
        
        if "ai" in role.lower():
            return json.dumps([
                {"skill": "Python", "status": "Present", "priority": "Low"},
                {"skill": "SQL", "status": "Present", "priority": "Low"},
                {"skill": "Machine Learning", "status": "Present", "priority": "Medium"},
                {"skill": "FastAPI", "status": "Missing", "priority": "High"},
                {"skill": "Docker", "status": "Missing", "priority": "High"},
                {"skill": "LLMs & RAG", "status": "Missing", "priority": "High"},
                {"skill": "DSA", "status": "Missing", "priority": "Medium"},
                {"skill": "Git", "status": "Present", "priority": "Low"},
                {"skill": "Linux", "status": "Present", "priority": "Low"}
            ], indent=2)
        else:
            return json.dumps([
                {"skill": "React", "status": "Missing", "priority": "High"},
                {"skill": "CSS/Tailwind", "status": "Present", "priority": "Low"},
                {"skill": "TypeScript", "status": "Missing", "priority": "High"},
                {"skill": "FastAPI", "status": "Present", "priority": "Medium"}
            ], indent=2)

    # 3. Personalized Study Plan / Roadmap
    elif "roadmap" in p_lower or "study_plan" in p_lower:
        return json.dumps({
            "Week 1: Foundations & Backend": [
                {"task": "Review DSA Arrays & HashMaps", "completed": False},
                {"task": "Build CRUD API with FastAPI", "completed": False},
                {"task": "Implement SQL Joins & Indexes", "completed": False}
            ],
            "Week 2: Containerization & DevOps": [
                {"task": "Dockerize the FastAPI Application", "completed": False},
                {"task": "Understand Docker Compose and multi-container environments", "completed": False},
                {"task": "Learn basic Git workflows (branching, merging)", "completed": False}
            ],
            "Week 3: Advanced AI & LLMs": [
                {"task": "Integrate OpenAI API with FastAPI", "completed": False},
                {"task": "Build a Simple RAG application using ChromaDB", "completed": False},
                {"task": "Deploy app locally with Docker-Compose", "completed": False}
            ]
        }, indent=2)

    # 4. Coding Question Generation
    elif "dsa question" in p_lower or "coding question" in p_lower or "leetcode" in p_lower:
        difficulty = "Medium"
        for line in p_lower.split("\n"):
            if "difficulty:" in line:
                if "easy" in line:
                    difficulty = "Easy"
                elif "hard" in line:
                    difficulty = "Hard"
                break
            
        topic = "Arrays"
        for line in p_lower.split("\n"):
            if "topic:" in line:
                if "string" in line:
                    topic = "Strings"
                elif "map" in line or "hash" in line:
                    topic = "HashMaps"
                elif "link" in line:
                    topic = "Linked Lists"
                elif "tree" in line:
                    topic = "Trees"
                elif "graph" in line:
                    topic = "Graphs"
                elif "dynamic" in line or "dp" in line:
                    topic = "Dynamic Programming"
                break
            
        from backend.utils.leetcode_questions import LEETCODE_QUESTIONS
        question = LEETCODE_QUESTIONS.get((difficulty, topic), LEETCODE_QUESTIONS[("Medium", "Arrays")])
        return json.dumps(question, indent=2)

    # 5. Coding Solution Evaluation
    elif "evaluate solution" in p_lower or "evaluate code" in p_lower:
        return json.dumps({
            "score": 90,
            "time_complexity": "O(N)",
            "space_complexity": "O(N) due to HashMap usage",
            "feedback": "Excellent solution! The code is clean and handles edge cases properly.",
            "passed": True,
            "suggestions": ["Consider checking if the input list is null or empty before executing logic."]
        }, indent=2)

    # 6. HR Interview Question Generation or Evaluation
    elif "hr interview" in p_lower or "hr question" in p_lower:
        if "evaluate answer" in p_lower or "score" in p_lower:
            return json.dumps({
                "score": 88,
                "feedback": "You clearly outlined your strengths and linked them to the job description. To improve, structure your challenges using the STAR method.",
                "strengths": ["Clear communication", "Relatable stories"],
                "weaknesses": ["Vague target metrics"],
                "next_question": "Why do you want to join our organization specifically?",
                "is_complete": False
            }, indent=2)
        else:
            return json.dumps({
                "question": "Tell me about yourself, your academic background, and what motivated you to pursue a career as an AI Engineer."
            }, indent=2)

    # 7. Technical Interview Question Generation or Evaluation
    elif "technical interview" in p_lower or "technical question" in p_lower:
        if "evaluate answer" in p_lower or "score" in p_lower:
            return json.dumps({
                "score": 75,
                "feedback": "The explanation of consistency hashing was correct, but you missed explaining how virtual nodes help distribute load evenly.",
                "strengths": ["Accurate core definition", "Good database schema understanding"],
                "weaknesses": ["Lacked explanation on caching replication and hashing rings"],
                "next_question": "Explain the difference between SQL indexing methods and how they affect query performance.",
                "is_complete": False
            }, indent=2)
        else:
            return json.dumps({
                "question": "In your 'Customer Loyalty Recommendation System' project, how did you handle Cold Start problems for new users?"
            }, indent=2)

    # 8. Central Evaluator
    elif "evaluate" in p_lower or "score" in p_lower:
        return json.dumps({
            "score": 86,
            "strengths": ["Strong structural layout", "Detailed technical highlights"],
            "weaknesses": ["Missing certification links", "No mention of unit testing frameworks"],
            "feedback": ["Great work overall, but you should add some testing frameworks like pytest or JUnit to make it production-ready."]
        }, indent=2)

    return "Mock response payload"
