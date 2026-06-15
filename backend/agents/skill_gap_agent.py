import json
import logging
from backend.utils.llm_helper import call_llm

logger = logging.getLogger(__name__)

class SkillGapAnalysisAgent:
    def analyze(self, current_skills: list[str], target_role: str, target_company: str | None = None) -> list[dict]:
        """Compares current skills with expected skills for the target role/company."""
        logger.info(f"Analyzing skill gap for role: {target_role}, company: {target_company}")
        
        # Define standard lists for typical placement roles to guide the LLM
        role_expectations = {
            "ai engineer": ["Python", "DSA", "SQL", "Machine Learning", "Deep Learning", "LLMs & RAG", "FastAPI", "Docker", "Git", "Linux"],
            "software engineer": ["Java" or "C++" or "Python", "DSA", "SQL", "OOPs", "System Design", "Git", "Linux", "Docker", "REST APIs"],
            "frontend engineer": ["JavaScript", "TypeScript", "React" or "Vue", "HTML5", "CSS3/Tailwind", "Git", "Webpack/Vite", "REST APIs"],
            "backend engineer": ["Python" or "Java" or "Node.js", "SQL", "NoSQL", "FastAPI" or "Spring Boot" or "Express", "Docker", "DSA", "System Design", "Git"]
        }
        
        # Try to find target expectations locally to enrich the prompt
        matched_key = "software engineer"
        role_lower = target_role.lower()
        for key in role_expectations.keys():
            if key in role_lower:
                matched_key = key
                break
                
        expected_skills = role_expectations[matched_key]
        
        prompt = f"""
        Compare the student's current skills with the expected skills for the target role and company.
        Target Role: {target_role}
        Target Company: {target_company or 'Any Product-based Company'}

        Current Skills:
        {current_skills}

        Industry Standard Expected Skills for this role:
        {expected_skills}

        Analyze which expected skills are missing. Return a JSON list of objects, where each object contains:
        1. "skill": string (name of the skill)
        2. "status": string ("Present" or "Missing")
        3. "priority": string ("High", "Medium", "Low") based on how critical the skill is for the role/company.

        Example output format:
        [
          {{"skill": "Python", "status": "Present", "priority": "Low"}},
          {{"skill": "FastAPI", "status": "Missing", "priority": "High"}}
        ]

        Return ONLY the raw JSON list of objects. Do not include markdown wraps.
        """

        response = call_llm(
            prompt=prompt,
            system_prompt="You are an expert technical recruiter analyzing skills and competency gaps.",
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
            logger.error(f"Failed to parse LLM response for skill gap analysis: {e}. Raw response: {response}")
            # Fallback based on expected skills
            result = []
            for skill in expected_skills:
                status = "Present" if skill.lower() in [s.lower() for s in current_skills] else "Missing"
                priority = "High" if status == "Missing" else "Low"
                result.append({"skill": skill, "status": status, "priority": priority})
            return result
        
