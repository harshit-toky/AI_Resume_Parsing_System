import spacy
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load spaCy model with word vectors
nlp = spacy.load("en_core_web_sm")  

# Predefined skills dictionary
predefined_skills = {"Python", "Java", "C++", "C", "JavaScript", "TypeScript", "Go", "Rust", "Swift", "Kotlin",
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
    "Jest", "Mocha", "Cypress", "Unity", "Unreal Engine", "Blender", "Javascript"}


def extract_resume_data(parsed_resume):
    """Extracts skills and education from parsed resume"""
    resume_skills = set(parsed_resume.get("skills", []))
    # resume_education = [edu["details"] for edu in parsed_resume.get("education", [])]
    # return resume_skills, resume_education
    return resume_skills


def extract_job_skills(job_description):
    """Extracts skills from job description based on predefined skills"""
    job_skills = {skill for skill in predefined_skills if skill.lower() in job_description.lower()}
    return job_skills


def extract_job_education(job_description):
    """Extracts education requirements from job description"""
    edu_keywords = ["bachelor", "master", "phd", "degree", "computer science", "software engineering"]
    job_education = {token.text for token in nlp(job_description.lower()) if token.text in edu_keywords}
    return job_education if job_education else {"Not Specified"}


# def compute_similarity(resume_skills, job_skills):
#     matched_skills = {}
#     unmatched_skills = []

#     for r_skill in resume_skills:
#         r_vec = nlp(r_skill).vector
#         if np.linalg.norm(r_vec) == 0:
#             continue  # Skip skills without valid vectors

#         best_match = None
#         best_score = 0

#         for j_skill in job_skills:
#             j_vec = nlp(j_skill).vector
#             if np.linalg.norm(j_vec) == 0:
#                 continue  # Skip invalid vectors

#             score = cosine_similarity([r_vec], [j_vec])[0][0]

#             if score > best_score:
#                 best_match, best_score = j_skill, score

#         if best_score >= 0.6:  # Adjust threshold if necessary
#             matched_skills[r_skill] = (best_match, round(best_score, 2))
#         else:
#             unmatched_skills.append(r_skill)

#     overall_similarity = round(sum(score for _, score in matched_skills.values()) / max(1, len(resume_skills)), 2)
#     # print(type(overall_similarity))
#     return matched_skills, unmatched_skills, overall_similarity
def compute_similarity(resume_skills, job_skills):
    matched_skills = {}
    unmatched_resume_skills = set(resume_skills)  # Keep track of resume skills that don’t match
    unmatched_job_skills = set(job_skills)  # Keep track of job skills missing in resume

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

        if best_score >= 0.95:  # Adjust threshold if necessary
            matched_skills[r_skill] = (best_match, round(best_score, 2))
            unmatched_resume_skills.discard(r_skill)  # Remove matched resume skills
            unmatched_job_skills.discard(best_match)  # Remove matched job skills

    # Update unmatched skills to include job skills missing from the resume
    unmatched_skills = {
        "resumeExtraSkills": list(unmatched_resume_skills),  # Skills in resume but not in job description
        "jobMissingSkills": list(unmatched_job_skills)  # Skills in job description but not in resume
    }

    # Calculate similarity score based on job skills
    total_skills = len(job_skills)
    overall_similarity = round(
        sum(score for _, score in matched_skills.values()) / max(1, total_skills), 2
    )
    if(overall_similarity > 1):
        overall_similarity = 1
    # print(matched_skills)
    # print(unmatched_skills["jobMissingSkills"])

    return matched_skills, unmatched_skills["jobMissingSkills"], overall_similarity


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


def analyze_resume(parsed_resume, job_description):
    
    resume_skills = extract_resume_data(parsed_resume)
    job_skills = extract_job_skills(job_description)
    # job_education = extract_job_education(job_description)

    matched_skills, unmatched_skills, skills_similarity = compute_similarity(resume_skills, job_skills)
    # matched_education, education_similarity = compare_education(resume_education, job_education)

    # Convert numpy.float32 values to Python float
    skills_similarity = float(skills_similarity)
    # print(type(skills_similarity))
    # education_similarity = float(education_similarity)

    # final_similarity_score = round(((skills_similarity + education_similarity) / 2) * 100, 2)

    # return (
    #     {key: (value[0], float(value[1])) for key, value in matched_skills.items()},  # Convert skill scores
    #     unmatched_skills,
    #     matched_education,
    #     job_education,
    #     float(final_similarity_score)  # Ensure final score is a Python float
    # )
    return {
        "matchedSkills": {key: (value[0], float(value[1])) for key, value in matched_skills.items()},  # Convert skill scores
        "unmatchedSkills": unmatched_skills,
        "similarityScore": round(skills_similarity * 100, 2)  # Convert to percentage
    }