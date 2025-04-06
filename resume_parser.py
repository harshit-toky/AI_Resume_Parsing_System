import re
import spacy
import json
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResumeParser:
    def __init__(self):
        # Load spaCy NLP model
        self.nlp = spacy.load("en_core_web_lg")

        # Regular expressions for common patterns
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        self.phone_pattern = r'(\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}'
        self.url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
        self.linkedin_pattern = r'linkedin\.com/in/[\w-]+'

        # Common skills dictionary
        self.skills_db = set([
            "python", "java", "javascript", "c++", "sql", "r", "machine learning",
            "data analysis", "excel", "tableau", "power bi", "html", "css", "react",
            "angular", "node.js", "aws", "azure", "docker", "kubernetes", "tensorflow",
            "pytorch", "nlp", "data science", "agile", "scrum", "project management",
            "leadership", "communication", "problem solving", "teamwork", "git"
        ])

        # Common education keywords
        self.education_keywords = [
            "university", "college", "institute", "academy", "school", "bachelor",
            "master", "phd", "doctorate", "degree", "b.tech", "m.tech", "bsc", "msc",
            "mba", "certification", "diploma"
        ]

        # Common job title keywords
        self.job_title_keywords = [
            "engineer", "developer", "manager", "director", "analyst", "specialist",
            "consultant", "coordinator", "assistant", "executive", "administrator",
            "technician", "supervisor", "lead", "head", "architect", "scientist"
        ]

    def lexical_analysis(self, text):
        """
        Perform lexical analysis (tokenization) on the resume text.
        Returns a list of tokens.
        """
        # Preprocess text (normalize whitespace)
        text = ' '.join(text.split())

        # Process with spaCy for advanced tokenization
        doc = self.nlp(text)

        # Extract tokens
        tokens = [token.text for token in doc]

        return tokens

    def syntax_analysis(self, text):
        """
        Perform syntax analysis to identify patterns like email, phone numbers, etc.
        """
        doc = self.nlp(text)

        # Extract basic patterns using regex
        email = re.findall(self.email_pattern, text)
        phone = re.findall(self.phone_pattern, text)
        urls = re.findall(self.url_pattern, text)
        linkedin = re.findall(self.linkedin_pattern, text)

        # Extract name (assuming it's one of the first named entities of type PERSON)
        potential_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        name = potential_names[0] if potential_names else ""

        # Extract skills
        skills = self.extract_skills(text)

        # Extract education
        education = self.extract_education(text)

        # Extract experience
        experience = self.extract_experience(text)

        return {
            "name": name,
            "email": email[0] if email else "",
            "phone": phone[0] if phone else "",
            "linkedin": linkedin[0] if linkedin else "",
            "skills": skills,
            "education": education,
            "experience": experience
        }

    def extract_skills(self, text):
        """
        Extract skills from the resume text.
        """
        doc = self.nlp(text.lower())
        skills = []

        # Check for skills in our database
        for token in doc:
            if token.text in self.skills_db:
                skills.append(token.text)

        # Check for multi-word skills
        for skill in self.skills_db:
            if len(skill.split()) > 1 and skill in text.lower():
                skills.append(skill)

        return list(set(skills))  # Remove duplicates

    def extract_education(self, text):
        """
        Extract education information from the resume.
        """
        education_info = []
        doc = self.nlp(text)

        # Split text into paragraphs
        paragraphs = re.split(r'\n\n|\r\n\r\n', text)

        for paragraph in paragraphs:
            # Check if paragraph contains education keywords
            if any(keyword in paragraph.lower() for keyword in self.education_keywords):
                # Extract dates (assuming they are in the format like 2015-2019)
                dates = re.findall(r'(19|20)\d{2}[- ](19|20)\d{2}|(19|20)\d{2}[- ]present', paragraph, re.IGNORECASE)

                # Extract institutions (assuming they are named entities of type ORG)
                org_entities = [ent.text for ent in self.nlp(paragraph).ents if ent.label_ == "ORG"]

                # Extract degree (assuming it contains education keywords)
                degree = ""
                for edu_kw in self.education_keywords:
                    if edu_kw in paragraph.lower():
                        # Try to extract the degree details
                        degree_pattern = re.compile(r'([A-Za-z]+\s*(in|of)?\s*[A-Za-z\s]+(' + edu_kw + r'))',
                                                    re.IGNORECASE)
                        degree_match = degree_pattern.search(paragraph)
                        if degree_match:
                            degree = degree_match.group(0)
                            break

                education_info.append({
                    "institution": org_entities[0] if org_entities else "",
                    "degree": degree,
                    "dates": dates[0] if dates else ""
                })

        return education_info

    def extract_experience(self, text):
        """
        Extract work experience information from the resume.
        """
        experience_info = []

        # Split text into paragraphs
        paragraphs = re.split(r'\n\n|\r\n\r\n', text)

        for paragraph in paragraphs:
            # Check if paragraph contains job title keywords
            if any(keyword in paragraph.lower() for keyword in self.job_title_keywords):
                # Extract dates (assuming they are in the format like 2015-2019 or 2015-present)
                dates = re.findall(r'(19|20)\d{2}[- ](19|20)\d{2}|(19|20)\d{2}[- ]present', paragraph, re.IGNORECASE)

                # Extract company names (assuming they are named entities of type ORG)
                doc = self.nlp(paragraph)
                org_entities = [ent.text for ent in doc.ents if ent.label_ == "ORG"]

                # Extract job title
                job_title = ""
                for title_kw in self.job_title_keywords:
                    if title_kw in paragraph.lower():
                        # Try to extract the job title
                        title_pattern = re.compile(r'([A-Za-z]+\s*' + title_kw + r')', re.IGNORECASE)
                        title_match = title_pattern.search(paragraph)
                        if title_match:
                            job_title = title_match.group(0)
                            break

                experience_info.append({
                    "company": org_entities[0] if org_entities else "",
                    "job_title": job_title,
                    "dates": dates[0] if dates else "",
                    "description": paragraph
                })

        return experience_info

    def semantic_analysis(self, parsed_data):
        """
        Perform semantic analysis to enhance the extracted information.
        """
        # Enhance extracted data with context

        # Check if name is missing but email exists
        if not parsed_data["name"] and parsed_data["email"]:
            # Try to extract name from email
            potential_name = parsed_data["email"].split('@')[0]
            parsed_data["name"] = potential_name.replace(".", " ").title()

        return parsed_data

    def intermediate_representation(self, parsed_data):
        """
        Convert parsed data to a structured JSON format.
        """
        return json.dumps(parsed_data, indent=2)

    def parse_resume(self, text):
        """
        Main function to parse resume text.
        """
        # Step 1: Tokenize the text (Lexical Analysis)
        tokens = self.lexical_analysis(text)

        # Step 2: Extract structured information (Syntax Analysis)
        parsed_data = self.syntax_analysis(text)

        # Step 3: Enhance extracted data with context (Semantic Analysis)
        enhanced_data = self.semantic_analysis(parsed_data)

        # Step 4: Convert to structured format (Intermediate Representation)
        structured_data = self.intermediate_representation(enhanced_data)

        return structured_data