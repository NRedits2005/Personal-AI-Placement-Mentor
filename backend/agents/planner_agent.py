import json
import logging
from backend.utils.llm_helper import call_llm

logger = logging.getLogger(__name__)

class PersonalizedRoadmapAgent:
    def generate_plan(self, skill_gaps: list[dict], target_role: str, target_company: str | None = None) -> dict:
        """Generates a structured study plan based on skill gaps."""
        logger.info(f"Generating personalized study roadmap for role: {target_role}")
        
        missing_skills = [item["skill"] for item in skill_gaps if item["status"] == "Missing"]
        high_priority = [item["skill"] for item in skill_gaps if item["status"] == "Missing" and item["priority"] == "High"]
        
        prompt = f"""
        Generate a personalized study roadmap for a student preparing for a placement interview.
        Target Role: {target_role}
        Target Company: {target_company or 'Any Product-based Company'}
        Missing Skills: {missing_skills}
        High Priority Gaps to Fill first: {high_priority}

        Construct a 3-week study roadmap. Break this down into weekly tasks.
        For each task, include a descriptive action item.

        Return strictly a JSON object where the keys are "Week 1", "Week 2", and "Week 3".
        Each key should contain a list of objects, where each object has:
        - "task": string (actionable study topic or task)
        - "completed": boolean (always default to false)

        Example structure:
        {{
          "Week 1: Foundations": [
            {{"task": "Study DSA Arrays & String manipulation", "completed": false}},
            {{"task": "Learn FastAPI routing and dependency injection", "completed": false}}
          ],
          "Week 2: Backend Development": [
            {{"task": "Learn how to build Docker container and run Docker Compose", "completed": false}}
          ]
        }}

        Return ONLY the raw JSON object. Do not wrap in markdown tags.
        """

        response = call_llm(
            prompt=prompt,
            system_prompt="You are a professional technical training planner and syllabus designer.",
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
            logger.error(f"Failed to parse LLM response for study plan generation: {e}. Raw response: {response}")
            # Fallback 3-week plan
            return {
                "Week 1: Core Fundamentals": [
                    {"task": f"Learn basics of {', '.join(missing_skills[:2]) if missing_skills else 'OOPs & Database'}", "completed": False},
                    {"task": "Solve 5 Easy DSA questions on Arrays/Strings", "completed": False},
                    {"task": "Create Git repository and push a basic coding script", "completed": False}
                ],
                "Week 2: Backend & System Integration": [
                    {"task": f"Build a prototype application integrating {missing_skills[2] if len(missing_skills) > 2 else 'FastAPI'}", "completed": False},
                    {"task": "Solve 5 Medium DSA questions on Stacks/Queues", "completed": False},
                    {"task": "Write basic SQL scripts to join multiple tables", "completed": False}
                ],
                "Week 3: Advanced Topics & Deployment": [
                    {"task": f"Deep dive into {missing_skills[3] if len(missing_skills) > 3 else 'System Design'}", "completed": False},
                    {"task": "Conduct a mock interview session", "completed": False},
                    {"task": "Deploy the prototype application using Docker containers", "completed": False}
                ]
            }
