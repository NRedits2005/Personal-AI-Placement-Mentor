import json
import logging
from backend.mcp.client import MCPClient
from backend.utils.llm_helper import call_llm

logger = logging.getLogger(__name__)

class ResumeAnalysisAgent:
    def __init__(self):
        self.mcp = MCPClient()

    def analyze(self, pdf_path: str, target_role: str | None = "Software Engineer") -> dict:
        """Parses the resume and calculates scores and suggestions."""
        logger.info(f"Analyzing PDF resume at path: {pdf_path}")
        
        # Read text from PDF via MCP
        resume_text = self.mcp.read_pdf(pdf_path)
        
        prompt = f"""
        Analyze the following resume text.
        Target Role: {target_role}

        Extract the following and return strictly a JSON object:
        1. "resume_score": integer (0 to 100 based on layout, depth, projects, readability)
        2. "ats_score": integer (0 to 100 based on keyword match, target role relevance)
        3. "skills": list of strings (programming languages, libraries, databases, tools)
        4. "missing_sections": list of strings (e.g. GitHub link, LinkedIn, Professional Summary, certifications)
        5. "improvement_suggestions": list of strings (actionable feedback to improve the resume)
        6. "github_url": string or null (if found in resume)
        7. "linkedin_url": string or null (if found in resume)

        Resume Text:
        ---
        {resume_text}
        ---

        Return ONLY a raw JSON object. Do not include markdown headers like ```json.
        """

        response = call_llm(
            prompt=prompt,
            system_prompt="You are a professional ATS resume reviewer and recruiter.",
            response_format="json"
        )

        try:
            # Clean possible markdown wrap if returned by some LLMs
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("\n", 1)[0]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
                
            return json.loads(cleaned)
        except Exception as e:
            logger.error(f"Failed to parse LLM response for resume analysis: {e}. Raw response: {response}")
            # Safe default
            return {
                "resume_score": 70,
                "ats_score": 70,
                "skills": ["Python", "Git"],
                "missing_sections": ["GitHub"],
                "improvement_suggestions": ["Ensure GitHub link is present."],
                "github_url": None,
                "linkedin_url": None
            }
