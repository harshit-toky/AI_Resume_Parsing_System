import requests
import re
from typing import Dict, List, Tuple
import spacy
from nltk.corpus import stopwords
import nltk

# Download NLTK data
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('stopwords')
    nltk.download('wordnet')

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

class ResumeAuthenticityChecker:
    def __init__(self, gptzero_api_key: str = None):
        self.gptzero_api_key = gptzero_api_key
        self.company_cache = {}  # Cache for company verification results

    def detect_ai_content(self, text: str) -> Tuple[float, bool]:
        """
        Detects AI-generated content using GPTZero API or a mock implementation.
        Returns (ai_score, is_suspected_ai).
        """
        if self.gptzero_api_key:
            try:
                response = requests.post(
                    "https://api.gptzero.me/v2/predict",
                    headers={"Authorization": f"Bearer {self.gptzero_api_key}"},
                    json={"document": text}
                )
                if response.status_code == 200:
                    result = response.json()
                    ai_score = result.get("document", {}).get("average_generated_prob", 0.0)
                    is_suspected_ai = ai_score > 0.7  # Threshold for suspicion
                    return ai_score, is_suspected_ai
            except Exception as e:
                print(f"Error in GPTZero API call: {e}")
                return 0.0, False
        else:
            # Mock implementation (heuristic-based)
            ai_indicators = ["perfect grammar", "generic phrasing", "buzzword heavy"]
            words = text.lower().split()
            buzzword_count = sum(1 for word in words if word in ["innovative", "synergy", "disruptive"])
            ai_score = buzzword_count / len(words) if words else 0.0
            is_suspected_ai = ai_score > 0.1
            return ai_score, is_suspected_ai

    def verify_company(self, company_name: str) -> bool:
        """
        Verifies if a company exists using a mock external API or cached data.
        In a real system, use services like Clearbit or LinkedIn API.
        """
        if company_name in self.company_cache:
            return self.company_cache[company_name]

        # Mock implementation: Check if company name seems realistic
        doc = nlp(company_name)
        is_valid = any(ent.label_ == "ORG" for ent in doc.ents)
        self.company_cache[company_name] = is_valid
        return is_valid

    def cross_reference_skills(self, skills: List[str], experience: List[Dict]) -> List[str]:
        """
        Checks if claimed skills are supported by experience.
        Returns a list of unsupported skills.
        """
        unsupported_skills = []
        experience_text = " ".join(
            [exp.get("description", "") + " " + exp.get("title", "") for exp in experience]
        ).lower()
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower not in experience_text and skill_lower not in stop_words:
                unsupported_skills.append(skill)
        return unsupported_skills

    def check_resume_authenticity(self, parsed_resume: Dict) -> Dict:
        """
        Main function to check resume authenticity.
        Input: Parsed resume as a dict (e.g., from pyresparser).
        Output: Dict with authenticity results.
        """
        result = {
            "ai_score": 0.0,
            "is_suspected_ai": False,
            "unsupported_skills": [],
            "invalid_companies": [],
            "authenticity_flags": []
        }

        # Extract raw text for AI detection
        raw_text = parsed_resume.get("raw_text", "")
        if raw_text:
            ai_score, is_suspected_ai = self.detect_ai_content(raw_text)
            result["ai_score"] = ai_score
            result["is_suspected_ai"] = is_suspected_ai
            if is_suspected_ai:
                result["authenticity_flags"].append("Suspected AI-generated content")

        # Cross-reference skills
        skills = parsed_resume.get("skills", [])
        experience = parsed_resume.get("experience", [])
        unsupported_skills = self.cross_reference_skills(skills, experience)
        result["unsupported_skills"] = unsupported_skills
        if unsupported_skills:
            result["authenticity_flags"].append(
                f"Skills without supporting experience: {', '.join(unsupported_skills)}"
            )

        # Verify company names
        for exp in experience:
            company = exp.get("company", "")
            if company and not self.verify_company(company):
                result["invalid_companies"].append(company)
                result["authenticity_flags"].append(f"Invalid company name: {company}")

        # Calculate overall authenticity score (simple heuristic)
        total_flags = len(result["authenticity_flags"])
        result["authenticity_score"] = max(0, 100 - (total_flags * 20))

        return result