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

# def extract_experience(tokens):
#     exp_keywords = ["Internship", "Experience", "Employment", "Job", "Work"]
#     experience = []
#     for i, token in enumerate(tokens):
#         if token in exp_keywords:
#             exp_entry = " ".join(tokens[i:i+30])  # Capture surrounding words
#             experience.append(exp_entry)
#             i += 30
#     return experience


def extract_experience_sections(tokens):
    all_headers = ['PROFILE', 'ACADEMIC DETAILS', 'Internship', 'Experience', 'PROJECTS', 
                   'TECHNICAL SKILLS', 'CERTIFICATIONS', 'ACHIEVEMENTS', 'POSITIONS OF RESPONSIBILITY']
    exp_keywords = ["Internship", "Experience", "Employment", "Job", "Work"]

    all_headers_lower = [h.lower() for h in all_headers]
    exp_keywords_lower = [k.lower() for k in exp_keywords]

    sections = []
    i = 0
    n = len(tokens)

    while i < n:
        token_lower = tokens[i].lower()

        if token_lower in exp_keywords_lower:
            current_header = token_lower
            section_tokens = [tokens[i]]
            i += 1

            while i < n:
                next_token_lower = tokens[i].lower()
                if next_token_lower in all_headers_lower and next_token_lower != current_header:
                    break
                section_tokens.append(tokens[i])
                i += 1

            section_text = " ".join(section_tokens)
            sections.append((current_header, section_text))
        else:
            i += 1

    return sections


def parse_experience(tokens):
    sections = extract_experience_sections(tokens)
    if not sections:
        return []

    # Ensure we're joining only strings
    section_text = "\n".join([str(text) for _, text in sections])

    # DEBUG: Check if section_text is actually a string
    assert isinstance(section_text, str), "section_text is not a string"

    entries = re.split(r'\n\s*•\s*', section_text)
    parsed_experience = []

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        lines = entry.split('\n')
        first_line = lines[0]
        
        title_match = re.match(r'^(.*?)\s*\(', first_line)
        date_match = re.search(r'\((.*?)\)', first_line)
        
        title = title_match.group(1).strip() if title_match else "Unknown Title"
        dates = date_match.group(1).strip() if date_match else "Unknown Dates"
        
        description_start = first_line.split(':', 1)[1] if ':' in first_line else ""
        description = (description_start.strip() + " " + " ".join(lines[1:])).strip()

        if title == "Unknown Title" and dates == "Unknown Dates" and description == "":
            continue

        parsed_experience.append({
            "title": title,
            "dates": dates,
            "description": description
        })

    return parsed_experience


def extract_projects(tokens):
    """Extract project details from tokenized resume text."""
    text = " ".join(tokens)

    pattern = r"(?:Projects|Personal Projects|Work Experience)\s*(.*?)(?=\n\n|Skills|Certifications|Education|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    if match:
        project_section = match.group(1).strip()

        # Modified regex with optional duration
        projects = re.findall(r"•\s*([^\n:•()]+?)\s*(?:\(([^)]+)\))?\s*:\s*(.*?)\s*(?=•|$)", project_section, re.DOTALL)

        parsed_projects = []
        for project in projects:
            title = project[0].strip()
            duration = project[1].strip() if project[1] else None
            description = " ".join(project[2].split()).strip()
            parsed_projects.append({
                "title": title,
                "duration": duration,
                "description": description
            })

        return parsed_projects if parsed_projects else None

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
def parse_resume(tokens, filePath):
    parsed_data = {
        "Name": extract_name(tokens),
        "Email": extract_email(tokens),
        "Phone": extract_phone(tokens),
        "Links": extract_links(tokens),
        "Education": extract_education(tokens),
        "Skills": extract_skills(tokens),
        "Experience": parse_experience(tokens),
        "Projects": extract_projects(tokens),
        "Certifications": extract_certifications(tokens)
    }

    # Display Results
    for key, value in parsed_data.items():
        print(f"{key}: {value}\n")

    create_json(parsed_data, filePath)


