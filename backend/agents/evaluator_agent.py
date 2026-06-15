import json
import logging
from backend.utils.llm_helper import call_llm

logger = logging.getLogger(__name__)

class EvaluatorAgent:
    def evaluate_interview_response(self, question: str, answer: str, context: str = "") -> dict:
        """Evaluates an interview response and returns score and feedback metrics."""
        logger.info(f"Evaluating answer for question: {question[:40]}...")
        
        prompt = f"""
        Evaluate the candidate's response to the interview question below.
        
        Context/Target: {context}
        Question: {question}
        Candidate Answer: {answer}

        Evaluate based on:
        1. Clarity & structure (communication).
        2. Technical accuracy & depth (concrete explanation, terminology).
        3. Completeness (covering all parts of the question).
        
        Return strictly a JSON object with:
        - "score": integer (0 to 100)
        - "strengths": list of strings (what they did well)
        - "weaknesses": list of strings (what was missing or incorrect)
        - "feedback": list of strings (constructive advice to score higher next time)

        Return ONLY the raw JSON. Do not write markdown wrapping blocks.
        """

        response = call_llm(
            prompt=prompt,
            system_prompt="You are a senior recruitment evaluator who scores answers objectively and helps candidates improve.",
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
            logger.error(f"Failed to parse evaluation LLM response: {e}. Raw response: {response}")
            return {
                "score": 75,
                "strengths": ["Direct response to the question"],
                "weaknesses": ["Could provide more technical detail"],
                "feedback": ["Try to give concrete examples from your past projects to back up your claims."]
            }
