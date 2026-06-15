import json
import logging
from backend.utils.llm_helper import call_llm

logger = logging.getLogger(__name__)

class HRInterviewAgent:
    def generate_question(self, student_profile: dict, history: list[dict] = []) -> dict:
        """Generates the next behavioral/HR question based on the student's background and chat history."""
        logger.info("Generating next HR mock question.")
        
        prompt = f"""
        Conduct a mock HR placement interview for a student.
        Student Details:
        - Name: {student_profile.get('full_name')}
        - Target Role: {student_profile.get('target_role')}
        - Target Company: {student_profile.get('target_company')}
        - College/Graduation: {student_profile.get('college')} ({student_profile.get('graduation_year')})

        Previous conversation:
        {history}

        Based on the current chat history, select or generate the next logical HR question.
        Typical questions:
        1. Tell me about yourself.
        2. Explain your strengths and weaknesses.
        3. Why should we hire you?
        4. Describe a challenging project situation and how you resolved it.
        5. Where do you see yourself in 5 years?

        If the history is empty, start with 'Tell me about yourself'.
        Otherwise, select a different topic.

        Return strictly a JSON object with:
        - "question": string (the question text)

        Return ONLY the raw JSON object. Do not include markdown labels.
        """

        response = call_llm(
            prompt=prompt,
            system_prompt="You are a professional HR Manager conducting interviews using the STAR methodology.",
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
            logger.error(f"Failed to parse HR question LLM response: {e}. Raw response: {response}")
            # Fallback questions based on history length
            questions = [
                "Tell me about yourself, your projects, and your aspirations as an engineer.",
                "What are your biggest strengths and weaknesses, and how do they impact your work?",
                "Why are you interested in joining your target company, and how do you align with its core values?",
                "Describe a situation where you had a conflict with a team member. How did you resolve it?",
                "Do you have any questions for me regarding this role?"
            ]
            index = min(len(history), len(questions) - 1)
            return {"question": questions[index]}
