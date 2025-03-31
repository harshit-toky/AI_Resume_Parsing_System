import re
import spacy
from validation import create_json

nlp = spacy.load("en_core_web_sm")
TECH_WORDS = {"C++", "Java", "Python", "HTML", "CSS", "JavaScript", "MySQL", "Git", "Mar"}

def extract_name(tokens):
    """Extracts the name from tokenized resume text."""
    text = " ".join(tokens)

    # Debug: Print first few tokens
    # print("\n🔹 Debug: First 50 Tokens:\n", tokens[:50])

    # Common patterns for name extraction
    possible_patterns = [
        r"Extracted\s*Text\s*:\s*(\w+\s+\w+)",  # Extracted Text: First Last
        r"^([\w]+\s[\w]+)(?=\s*Email|Email\-id|Mobile)",  # Name before Email
        r"([\w]+\s[\w]+)(?=\s*B\.\s?Tech|Bachelors|M\.Tech|Masters|Degree)",  # Name before education
    ]

    for pattern in possible_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # print("\n✅ Extracted Name:", name)
            return name

    # print("\n❌ Name Not Found")
    return None


def extract_email(tokens):
    for token in tokens:
        if re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", token):
            return token
    return None

def extract_phone(tokens):
    for token in tokens:
        if re.match(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", token):
            return token
    return None

def extract_links(tokens):
    return [token for token in tokens if token.startswith("http")]

def extract_education(tokens):
    edu_keywords = ["B.Tech", "M.Tech", "Bachelor", "Master", "Ph.D", "Diploma", "12th", "10th"]
    education = []
    for i, token in enumerate(tokens):
        if token in edu_keywords:
            edu_entry = " ".join(tokens[i:i+5])  # Capture surrounding words
            education.append(edu_entry)
    return education

def extract_skills(tokens):
    predefined_skills = {
        "python", "java", "c++", "c", "javascript", "typescript", "go", "rust", "swift", "kotlin",
        "sql", "nosql", "postgresql", "mysql", "mongodb", "redis", "sqlite", "oracledb", "graphql", 
        "pl/sql", "firebase", "machine learning", "deep learning", "data structures", "algorithms", 
        "computer vision", "opencv", "tensorflow", "keras", "pytorch", "scikit-learn", "pandas", 
        "numpy", "matplotlib", "seaborn", "nltk", "spacy", "hugging face transformers", "flask", 
        "django", "fastapi", "spring boot", "express.js", "node.js", "react", "next.js", "angular", 
        "vue.js", "svelte", "bootstrap", "tailwind css", "material-ui", "jquery", "three.js", 
        "webassembly", "graphql", "rest api", "microservices", "docker", "kubernetes", "git", 
        "github", "gitlab", "ci/cd", "jenkins", "terraform", "ansible", "aws", "azure", "google cloud", 
        "linux", "shell scripting", "bash", "powershell", "operating systems", "embedded systems", 
        "cybersecurity", "cryptography", "blockchain", "smart contracts", "solidity", "ethereum", 
        "hyperledger", "arduino", "raspberry pi", "computer networks", "network security", "devops", 
        "agile", "scrum", "data science", "big data", "hadoop", "spark", "kafka", "airflow", 
        "natural language processing", "reinforcement learning", "generative ai", "llms", "automl", 
        "data engineering", "etl", "snowflake", "data warehousing", "elk stack", "selenium", 
        "jest", "mocha", "cypress", "unity", "unreal engine", "blender"
    }

    return [token for token in tokens if token.lower() in predefined_skills]


def extract_experience(tokens):
    exp_keywords = ["Internship", "Experience", "Employment", "Job", "Work"]
    experience = []
    for i, token in enumerate(tokens):
        if token in exp_keywords:
            exp_entry = " ".join(tokens[i:i+10])  # Capture surrounding words
            experience.append(exp_entry)
    return experience

def extract_projects(tokens):
    """Extract project details from tokenized resume text."""
    text = " ".join(tokens)

    # Debug: Print full resume text
    # print("\nFull Resume Text:\n", text[:1000])

    # Regex pattern to find projects section
    pattern = r"(?:Projects|Personal Projects|Work Experience)\s*(.*?)(?=\n\n|Skills|Certifications|Education|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    if match:
        project_section = match.group(1).strip()

        # Debug: Print extracted projects section
        # print("\nExtracted Projects Section:\n", project_section[:500])

        # New Regex for extracting projects
        projects = re.findall(r"•\s*([\w\s]+?)\s*\(([^)]+)\)\s*:\s*(.*?)\s*(?=•|$)", project_section, re.DOTALL)

        parsed_projects = []
        for project in projects:
            title, duration, description = project
            parsed_projects.append({
                "title": title.strip(),
                "duration": duration.strip(),
                "description": " ".join(description.split()).strip()
            })

        # Debug: Print extracted project details
        # print("\nParsed Projects:\n", parsed_projects)

        return parsed_projects if parsed_projects else None

    # print("\n❌ No Projects Found")
    return None



def extract_certifications(tokens):
    """Extract certifications based on keywords."""
    text = " ".join(tokens)
    pattern = r"(Certifications|Certified|Successfully completed|Attained)(.*?)(?=\n\n|Projects|Experience|Skills|Education|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    if match:
        return match.group(2).strip().split("\n")  # Return list of certifications
    return None

# Extract Information from Tokenized Data
def parse_resume(tokens):
    parsed_data = {
        "Name": extract_name(tokens),
        "Email": extract_email(tokens),
        "Phone": extract_phone(tokens),
        "Links": extract_links(tokens),
        "Education": extract_education(tokens),
        "Skills": extract_skills(tokens),
        "Experience": extract_experience(tokens),
        "Projects": extract_projects(tokens),
        "Certifications": extract_certifications(tokens)
    }

    # Display Results
    for key, value in parsed_data.items():
        print(f"{key}: {value}\n")

    create_json(parsed_data)
