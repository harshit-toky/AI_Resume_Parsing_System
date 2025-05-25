import re
from typing import Dict, List, Tuple
import spacy
from nltk.corpus import stopwords
import nltk

# Download NLTK data (Colab-compatible)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Load SpaCy model (available in Colab)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model not found. Run: !pip install spacy && python -m spacy download en_core_web_sm")
    raise

stop_words = set(stopwords.words('english'))

class ResumeAuthenticityChecker:
    def __init__(self):
        self.company_cache = {}  # Cache for company verification results
        self.buzzwords = [
            "game-changer", "disruptive", "leverage", "synergy", "cutting-edge",
            "paradigm", "streamlined", "holistic", "next-gen", "transformative"
        ]  # AI-related buzzwords
        self.major_tech_companies = [
            "Google", "Amazon", "Microsoft", "Apple", "Facebook", "Meta", "Tesla", 
            "Intel", "IBM", "Oracle", "Cisco", "Nvidia", "Adobe", "Salesforce", 
            "Amazon Web Services", "AWS", "Accenture", "Deloitte", "Tata Consultancy Services", 
            "TCS", "Infosys", "Wipro", "Cognizant", "Capgemini", "HCL Technologies",
            "Qualcomm", "SAP", "VMware", "ServiceNow", "PayPal", "Intuit", "Atlassian",
            "Snowflake", "Databricks", "Palantir", "Epic Systems", "Workday"
        ]  # List of major tech companies

    def detect_ai_content(self, text: str) -> Tuple[float, bool, List[str]]:
        """
        Heuristic-based detection of AI-generated content.
        Returns (ai_score, is_suspected_ai, triggered_buzzwords).
        """
        words = text.lower().split()
        if not words:
            return 0.0, False, []
        
        # Count buzzwords and track which ones are found
        buzzword_count = 0
        triggered_buzzwords = []
        for word in words:
            if word in self.buzzwords and word not in triggered_buzzwords:
                buzzword_count += 1
                triggered_buzzwords.append(word)
        
        # Calculate sentence length uniformity
        sentence_lengths = [len(sent.split()) for sent in text.split('.') if sent.strip()]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        sentence_uniformity = (
            sum(1 for length in sentence_lengths if abs(length - avg_sentence_length) < 3) / 
            len(sentence_lengths) if sentence_lengths else 0
        )
        
        # Check for generic phrases (e.g., lack of specific tools or numbers)
        generic_score = 1.0 if not any(char.isdigit() for char in text) else 0.5
        
        # Combine scores: buzzword density (50%), sentence uniformity (30%), generic phrasing (20%)
        buzzword_density = buzzword_count / len(words) if words else 0.0
        ai_score = (buzzword_density * 0.5 + sentence_uniformity * 0.3 + generic_score * 0.2)
        is_suspected_ai = ai_score > 0.5  # Threshold as requested
        
        return ai_score, is_suspected_ai, triggered_buzzwords

    def verify_company(self, company_name: str) -> bool:
        """
        Heuristic-based company name verification using SpaCy and major tech companies list.
        """
        if not company_name:
            return False
        if company_name in self.company_cache:
            return self.company_cache[company_name]

        # Check if the name matches a major tech company
        company_name_lower = company_name.lower()
        is_major_tech = any(tech_company.lower() in company_name_lower for tech_company in self.major_tech_companies)
        
        # Use SpaCy to check if the name is recognized as an organization
        doc = nlp(company_name)
        is_org = any(ent.label_ == "ORG" for ent in doc.ents)
        
        # Check for common company name endings
        company_patterns = r"(Inc\.|LLC|Corp\.|Corporation| Ltd\.| GmbH| Solutions| Technologies| Systems)$"
        has_company_pattern = bool(re.search(company_patterns, company_name, re.IGNORECASE))
        
        is_valid = is_major_tech or is_org or has_company_pattern
        self.company_cache[company_name] = is_valid
        return is_valid

    def cross_reference_skills(self, skills: List[str], experience: List[Dict], projects: List[Dict]) -> List[str]:
        """
        Checks if claimed skills are supported by experience or projects.
        Returns a list of unsupported skills.
        """
        unsupported_skills = []
        # Combine experience and project descriptions
        experience_text = " ".join(
            [exp.get("details", "") + " " + exp.get("role", "") for exp in experience]
        ).lower()
        project_text = " ".join(
            [proj.get("description", "") + " " + proj.get("title", "") for proj in projects]
        ).lower()
        combined_text = experience_text + " " + project_text

        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower not in combined_text and skill_lower not in stop_words:
                unsupported_skills.append(skill)
        return unsupported_skills

    def check_resume_authenticity(self, parsed_resume: Dict) -> Dict:
        """
        Main function to check resume authenticity.
        Input: Parsed resume as a dict.
        Output: Dict with authenticity results.
        """
        result = {
            "ai_score": 0.0,
            "is_suspected_ai": False,
            "triggered_buzzwords": [],
            "unsupported_skills": [],
            "invalid_companies": [],
            "authenticity_flags": []
        }

        # Extract text for AI detection
        raw_text = " ".join(
            [exp.get("details", "") + " " + exp.get("role", "") for exp in parsed_resume.get("experience", [])] +
            [proj.get("description", "") + " " + proj.get("title", "") for proj in parsed_resume.get("projects", [])]
        )
        if raw_text:
            ai_score, is_suspected_ai, triggered_buzzwords = self.detect_ai_content(raw_text)
            result["ai_score"] = ai_score
            result["is_suspected_ai"] = is_suspected_ai
            result["triggered_buzzwords"] = triggered_buzzwords
            if is_suspected_ai:
                result["authenticity_flags"].append(
                    f"Suspected AI-generated content (buzzwords: {', '.join(triggered_buzzwords)})"
                )

        # Cross-reference skills
        skills = parsed_resume.get("skills", [])
        experience = parsed_resume.get("experience", [])
        projects = parsed_resume.get("projects", [])
        unsupported_skills = self.cross_reference_skills(skills, experience, projects)
        result["unsupported_skills"] = unsupported_skills
        if unsupported_skills:
            result["authenticity_flags"].append(
                f"Skills without supporting experience or projects: {', '.join(unsupported_skills)}"
            )

        # Verify company names
        for exp in experience:
            company = exp.get("details", "").split("\n")[0].strip()
            if company and not self.verify_company(company):
                result["invalid_companies"].append(company)
                result["authenticity_flags"].append(f"Invalid or unverifiable company: {company}")

        # Calculate overall authenticity score
        total_flags = len(result["authenticity_flags"])
        result["authenticity_score"] = max(0, 100 - (total_flags * 20))

        return result