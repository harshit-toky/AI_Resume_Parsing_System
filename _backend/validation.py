import json
import re
import spacy
from fuzzywuzzy import process

nlp = spacy.load("en_core_web_sm")

# Predefined Skills & Degrees for validation
TECH_SKILLS = {"Python", "Java", "C++", "C", "Git", "OpenCV", "Machine Learning", "Deep Learning", "SQL", "React"}
DEGREES = {"B.Tech", "M.Tech", "B.Sc", "M.Sc", "PhD", "MBA", "BCA", "MCA"}

# Function to clean education details
def clean_education(education_list):
    structured_edu = []
    for edu in education_list:
        degree_match = next((d for d in DEGREES if d in edu), None)
        if degree_match:
            structured_edu.append({"degree": degree_match, "details": edu})
        else:
            structured_edu.append({"degree": "Unknown", "details": edu})
    return structured_edu

# Function to clean skills (remove duplicates)
def clean_skills(skill_list):
    return list(set(skill_list))

# Function to separate certifications from achievements
def clean_certifications(cert_list):
    certifications = []
    achievements = []
    for cert in cert_list:
        if "certification" in cert.lower() or "completed" in cert.lower():
            certifications.append(cert)
        elif "rank" in cert.lower() or "finalist" in cert.lower():
            achievements.append(cert)
    return certifications, achievements

# Function to clean experience details
def clean_experience(exp_list):
    structured_exp = []
    for exp in exp_list:
        match = re.search(r"(.*?)\((.*?)\)", exp)  # Extracts role and duration
        if match:
            structured_exp.append({"role": match.group(1).strip(), "duration": match.group(2).strip()})
        else:
            structured_exp.append({"role": "Unknown", "details": exp})
    return structured_exp

# Function to generate structured JSON
def create_json(parsed_data):
    certifications, achievements = clean_certifications(parsed_data["Certifications"])
    
    final_data = {
        "name": parsed_data["Name"],
        "email": parsed_data["Email"],
        "phone": parsed_data["Phone"],
        "links": parsed_data["Links"] if parsed_data["Links"] else None,
        "education": clean_education(parsed_data["Education"]),
        "skills": clean_skills(parsed_data["Skills"]),
        "experience": clean_experience(parsed_data["Experience"]),
        "projects": parsed_data["Projects"],
        "certifications": certifications,
        "achievements": achievements
    }
    print(final_data)
    save_to_json(final_data)


def save_to_json(data, filename="resume_parsed_data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"✅ Parsed data saved to {filename}")

# Load from JSON file
def load_from_json(filename="resume_parsed_data.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

