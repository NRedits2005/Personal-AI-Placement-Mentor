import json
import logging
from backend.utils.llm_helper import call_llm

logger = logging.getLogger(__name__)

class TechnicalInterviewAgent:
    def generate_question(self, student_profile: dict, resume_summary: dict = {}, github_projects: list[dict] = [], history: list[dict] = []) -> dict:
        """Generates project-specific and tech stack-specific interview questions."""
        logger.info("Generating next Technical mock question.")
        
        project_names = [p.get("name") for p in github_projects]
        extracted_skills = resume_summary.get("skills", [])
        
        prompt = f"""
        Conduct a mock technical placement interview.
        Student Details:
        - Target Role: {student_profile.get('target_role')}
        - Target Company: {student_profile.get('target_company')}
        - Extracted Resume Skills: {extracted_skills}
        - Analyzed GitHub Projects: {project_names}

        Previous Interview turns:
        {history}

        Based on the projects list, skills, and chat history, ask the next technical question.
        Focus on:
        1. Architecture design of one of their projects.
        2. Trade-offs (e.g. SQL vs NoSQL, Flask vs FastAPI).
        3. Scalability, caching (Redis), concurrency.
        4. Coding paradigms or core DSA concepts relevant to their stack.

        If history is empty, start with a comprehensive project architecture question (e.g., 'Describe the architecture of your project and your engineering decisions').
        Otherwise, drill deeper into their last response.

        Return strictly a JSON object with:
        - "question": string (the technical question text)

        Return ONLY the raw JSON. Do not include markdown code block wraps.
        """

        response = call_llm(
            prompt=prompt,
            system_prompt="You are a principal architect and lead interviewer conducting deep technical assessments.",
            response_format="json"
        )

        try:
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("\n", 1)[0]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
                
            return json.loads(cleaned)
        except Exception as e:
            logger.error(f"Failed to parse technical question LLM response: {e}. Raw response: {response}")
            # Fallback based on profile
            questions = [
                f"Describe the system architecture of your primary project. What technologies did you choose and why?",
                f"In your tech stack ({', '.join(extracted_skills[:3]) if extracted_skills else 'Python/SQL'}), how do you handle security and data persistence?",
                f"If you had to scale your application to handle 10,000 requests per second, what bottlenecks would you expect and how would caching help?",
                f"Explain how you would design a REST API to support search auto-complete functionality for a large catalog.",
                f"Do you have experience with concurrency? Explain async/await in Python or multi-threading."
            ]
            index = min(len(history), len(questions) - 1)
            return {"question": questions[index]}
