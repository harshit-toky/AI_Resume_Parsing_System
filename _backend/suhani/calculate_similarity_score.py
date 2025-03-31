import spacy
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load spaCy model with word vectors
nlp = spacy.load("en_core_web_lg")  # Use "en_core_web_lg" for better accuracy

# Predefined skills dictionary
predefined_skills ={
    "Python", "Java", "C++", "C", "JavaScript", "TypeScript", "Go", "Rust", "Swift", "Kotlin",
    "SQL", "NoSQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "OracleDB", "GraphQL",
    "PL/SQL", "Firebase", "Machine Learning", "Deep Learning", "Data Structures", "Algorithms",
    "Computer Vision", "OpenCV", "TensorFlow", "Keras", "PyTorch", "Scikit-learn", "Pandas",
    "NumPy", "Matplotlib", "Seaborn", "NLTK", "spaCy", "Hugging Face Transformers", "Flask",
    "Django", "FastAPI", "Spring Boot", "Express.js", "Node.js", "React", "Next.js", "Angular",
    "Vue.js", "Svelte", "Bootstrap", "Tailwind CSS", "Material-UI", "jQuery", "Three.js",
    "WebAssembly", "GraphQL", "REST API", "Microservices", "Docker", "Kubernetes", "Git",
    "GitHub", "GitLab", "CI/CD", "Jenkins", "Terraform", "Ansible", "AWS", "Azure", "Google Cloud",
    "Linux", "Shell Scripting", "Bash", "PowerShell", "Operating Systems", "Embedded Systems",
    "Cybersecurity", "Cryptography", "Blockchain", "Smart Contracts", "Solidity", "Ethereum",
    "Hyperledger", "Arduino", "Raspberry Pi", "Computer Networks", "Network Security", "DevOps",
    "Agile", "Scrum", "Data Science", "Big Data", "Hadoop", "Spark", "Kafka", "Airflow",
    "Natural Language Processing", "Reinforcement Learning", "Generative AI", "LLMs", "AutoML",
    "Data Engineering", "ETL", "Snowflake", "Data Warehousing", "ELK Stack", "Selenium",
    "Jest", "Mocha", "Cypress", "Unity", "Unreal Engine", "Blender"
}

def load_json(file_path):
    """Loads JSON data from a file"""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_text(file_path):
    """Loads text data from a file"""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_resume_data(parsed_resume):
    """Extracts skills and education from parsed resume"""
    resume_skills = set(parsed_resume.get("skills", []))
    resume_education = [edu["details"] for edu in parsed_resume.get("education", [])]
    return resume_skills, resume_education

def extract_job_skills(job_description):
    """Extracts skills from job description based on predefined skills"""
    doc = nlp(job_description.lower())
    job_skills = set()

    for skill in predefined_skills:
        if skill.lower() in job_description.lower():
            job_skills.add(skill)

    return job_skills


def extract_job_education(job_description):
    """Extracts education requirements from job description"""
    edu_keywords = ["bachelor", "master", "phd", "degree", "computer science", "software engineering"]
    doc = nlp(job_description.lower())
    job_education = {token.text for token in doc if token.text in edu_keywords}
    return job_education if job_education else {"Not Specified"}

def compute_similarity(resume_skills, job_skills):
    matched_skills = {}
    unmatched_skills = []

    for r_skill in resume_skills:
        r_vec = nlp(r_skill).vector
        if np.linalg.norm(r_vec) == 0:
            continue  # Skip skills without valid vectors

        best_match = None
        best_score = 0

        for j_skill in job_skills:
            j_vec = nlp(j_skill).vector
            if np.linalg.norm(j_vec) == 0:
                continue  # Skip invalid vectors

            score = cosine_similarity([r_vec], [j_vec])[0][0]

            if score > best_score:
                best_match, best_score = j_skill, score

        if best_score >= 0.6:  # Adjust threshold if necessary
            matched_skills[r_skill] = (best_match, round(best_score, 2))
        else:
            unmatched_skills.append(r_skill)

    overall_similarity = round(sum(score for _, score in matched_skills.values()) / max(1, len(resume_skills)), 2)
    return matched_skills, unmatched_skills, overall_similarity


def compare_education(resume_education, job_education):
    """Compares resume education with job education"""
    matched_education = None
    best_score = 0

    for r_edu in resume_education:
        r_vec = nlp(r_edu).vector.reshape(1, -1)

        for j_edu in job_education:
            j_vec = nlp(j_edu).vector.reshape(1, -1)
            score = cosine_similarity(r_vec, j_vec)[0][0]

            if score > best_score:
                matched_education, best_score = r_edu, score

    return matched_education if best_score >= 0.7 else None, round(best_score, 2)

# File Paths (Update these paths accordingly)
resume_file = "resume_parsed_data.json"  # JSON file containing parsed resume
job_desc_file = "job_desc.txt"  # Text file containing job description

# Load files
parsed_resume = load_json(resume_file)
job_description = load_text(job_desc_file)

# Extract data
resume_skills, resume_education = extract_resume_data(parsed_resume)
job_skills = extract_job_skills(job_description)
job_education = extract_job_education(job_description)

# Compute similarity
matched_skills, unmatched_skills, skills_similarity = compute_similarity(resume_skills, job_skills)
matched_education, education_similarity = compare_education(resume_education, job_education)

# Calculate final similarity percentage
final_similarity_score = round(((skills_similarity + education_similarity) / 2) * 100, 2)

# Print Results
print("\n🔹 Matched Skills:")
print(f"  ✅ {', '.join(matched_skills.keys()) if matched_skills else 'None'}")

print("\n🔹 Unmatched Skills:")
print(f"  ❌ {', '.join(unmatched_skills) if unmatched_skills else 'None'}")

print("\n🔹 Matched Education:")
if matched_education:
    print(f"  ✅ {matched_education}")
else:
    print(f"  ❌ No matching education found! Job requires: {', '.join(job_education)}")

print(f"\n📊 Overall Resume Match Score: {final_similarity_score}%")
