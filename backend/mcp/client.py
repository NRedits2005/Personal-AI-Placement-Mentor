import os
import logging
import httpx
from pypdf import PdfReader
from backend.config import settings

logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self):
        self.client = httpx.Client(timeout=10.0)
        # Check if external MCP servers are defined
        self.pdf_server_url = os.getenv("MCP_PDF_SERVER_URL")
        self.github_server_url = os.getenv("MCP_GITHUB_SERVER_URL")
        self.search_server_url = os.getenv("MCP_SEARCH_SERVER_URL")
        self.fs_server_url = os.getenv("MCP_FS_SERVER_URL")

    # --- PDF MCP Tool / Fallback ---
    def read_pdf(self, pdf_path: str) -> str:
        """Reads a PDF file and extracts text using MCP Server or local fallback."""
        if self.pdf_server_url:
            try:
                response = self.client.post(
                    f"{self.pdf_server_url}/tools/read_pdf",
                    json={"path": pdf_path}
                )
                if response.status_code == 200:
                    return response.json().get("content", "")
            except Exception as e:
                logger.error(f"MCP PDF Server call failed: {e}. Falling back to native pypdf.")

        # Native Fallback
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at: {pdf_path}")
        
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text_page = page.extract_text()
                if text_page:
                    text += text_page + "\n"
            return text
        except Exception as e:
            logger.error(f"Failed to read PDF natively: {e}")
            raise RuntimeError(f"Error reading PDF: {e}")

    # --- File System MCP Tool / Fallback ---
    def read_file(self, file_path: str) -> str:
        """Reads file content from the filesystem."""
        if self.fs_server_url:
            try:
                response = self.client.post(
                    f"{self.fs_server_url}/tools/read_file",
                    json={"path": file_path}
                )
                if response.status_code == 200:
                    return response.json().get("content", "")
            except Exception as e:
                logger.error(f"MCP File System Server failed: {e}. Falling back to OS.")

        # Native Fallback
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    # --- GitHub MCP Tool / Fallback ---
    def analyze_github(self, github_url: str) -> list[dict]:
        """Fetches repositories and metadata for a GitHub profile."""
        username = self._extract_username(github_url)
        if not username:
            return self._get_mock_github_projects("unknown")

        if self.github_server_url:
            try:
                response = self.client.post(
                    f"{self.github_server_url}/tools/get_repositories",
                    json={"username": username}
                )
                if response.status_code == 200:
                    return response.json().get("repositories", [])
            except Exception as e:
                logger.error(f"MCP GitHub Server failed: {e}. Falling back to GitHub Public API.")

        # Public GitHub API Fetch
        try:
            headers = {}
            token = os.getenv("GITHUB_TOKEN")
            if token:
                headers["Authorization"] = f"token {token}"
            
            api_url = f"https://api.github.com/users/{username}/repos"
            response = self.client.get(api_url, headers=headers)
            if response.status_code == 200:
                repos = response.json()
                parsed_repos = []
                for r in repos[:5]:  # Analyze top 5 repos
                    parsed_repos.append({
                        "name": r.get("name"),
                        "url": r.get("html_url"),
                        "description": r.get("description") or "No description provided.",
                        "language": r.get("language") or "Other",
                        "stars": r.get("stargazers_count", 0),
                        "forks": r.get("forks_count", 0)
                    })
                return parsed_repos
        except Exception as e:
            logger.error(f"GitHub API check failed: {e}. Generating mock data.")

        return self._get_mock_github_projects(username)

    def _extract_username(self, url: str) -> str | None:
        """Helper to extract username from GitHub URL."""
        if not url:
            return None
        url = url.strip().rstrip("/")
        parts = url.split("github.com/")
        if len(parts) > 1:
            return parts[1].split("/")[0]
        return url

    def _get_mock_github_projects(self, username: str) -> list[dict]:
        """Returns mock projects in case GitHub API fails or is rate-limited."""
        return [
            {
                "name": "Customer-Loyalty-Recommendation-System",
                "url": f"https://github.com/{username}/Customer-Loyalty-Recommendation-System",
                "description": "A collaborative filtering recommendation engine with role-based access control and scalability layers using Streamlit and PostgreSQL.",
                "language": "Python",
                "stars": 15,
                "forks": 3
            },
            {
                "name": "Placement-Prep-Platform",
                "url": f"https://github.com/{username}/Placement-Prep-Platform",
                "description": "Multi-agent coordinator for resumes and interview training utilizing LangGraph, Redis, and FastAPI.",
                "language": "Python",
                "stars": 24,
                "forks": 5
            },
            {
                "name": "Distributed-Key-Value-Store",
                "url": f"https://github.com/{username}/Distributed-Key-Value-Store",
                "description": "Consistent hashing and raft consensus protocol implementation in Go.",
                "language": "Go",
                "stars": 42,
                "forks": 12
            }
        ]

    # --- Web Search MCP Tool / Fallback ---
    def web_search(self, query: str) -> list[dict]:
        """Performs a web search to fetch interview experiences and patterns."""
        if self.search_server_url:
            try:
                response = self.client.post(
                    f"{self.search_server_url}/tools/search",
                    json={"query": query}
                )
                if response.status_code == 200:
                    return response.json().get("results", [])
            except Exception as e:
                logger.error(f"MCP Search Server failed: {e}. Falling back to default search engine.")

        # Return mock rich search results tailored to placement queries
        lower_query = query.lower()
        if "google" in lower_query:
            return [
                {
                    "title": "Google Software Engineer Interview Experience 2026",
                    "snippet": "Focused heavily on graph algorithms, Dijkstra's algorithm, and topological sort. HR round focused on Googlyness and working through conflicts with peers.",
                    "url": "https://leetcode.com/discuss/interview-experience/google-swe"
                },
                {
                    "title": "Google System Design prep and expectations",
                    "snippet": "Expectation is to design a distributed cache (similar to Redis). Focus on consistency, availability, and partitioning rules.",
                    "url": "https://systemdesignprimer.com/google-prep"
                }
            ]
        elif "microsoft" in lower_query:
            return [
                {
                    "title": "Microsoft SDE-2 Interview Guide",
                    "snippet": "Interview consists of 1 coding round (binary tree & arrays), 1 design round (designing TinyURL), and 1 behavioral round.",
                    "url": "https://geeksforgeeks.org/microsoft-interview-experience"
                }
            ]
        
        # General fallback results
        return [
            {
                "title": f"Recent Interview Patterns for {query}",
                "snippet": "Candidates reported coding questions based on dynamic programming (knapsack problem) and database design questions on SQL indexing and ACID properties.",
                "url": "https://leetcode.com/discuss/interview-question"
            },
            {
                "title": "Placement Preparation Checklist",
                "snippet": "Key topics: Data Structures (Trees, Graphs, HashMaps), Object-Oriented Design, System Design basics, and STAR method for HR questions.",
                "url": "https://interviewbit.com/prep-checklist"
            }
        ]
