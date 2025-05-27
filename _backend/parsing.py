import spacy
from syntaxAnalysis import parse_resume

nlp = spacy.load("en_core_web_sm")

def tokenize_resume(text, filePath):
    doc = nlp(text)
    tokens = [token.text for token in doc]
    save_tokens_to_file(tokens)
    parse_resume(tokens, filePath)
    return tokens

def save_tokens_to_file(tokens, filename="tokenized_resume.txt"):
    """Save tokenized resume data in a structured format with double quotes and commas."""
    with open(filename, "w", encoding="utf-8") as file:
        formatted_tokens = ", ".join(f'"{token}"' for token in tokens)  # Enclose each token in double quotes
        file.write(formatted_tokens)
    print(f"✅ Tokenized data saved to {filename}")

# text = """ Harshit Toky
# Email-id : tokyharshit0@gmail.com
# Mobile No.: 9817610471,
# https://www.linkedin.com/in/harshit-toky-4126b02a6/
# https://github.com/harshit-toky
# PROFILE
# • I am currently pursuing my Bachelor’s degree in Computer Science and Engineering (CSE) at Graphic
# Era University. With a strong foundation in programming, Experienced in designing and implementing
# scalable, efficient solutions using C++ and Java, with hands-on expertise in game development and software
# engineering.
# ACADEMIC DETAILS
# Year Degree/Exam Institute GPA/Marks(%)
# Sep, 2022 - Jun, 2026 B.TECH in Computer Science Graphic Era University Dehradun 9.58/10
# 2021 12th, C.B.S.E Aggarsain Public School 91.00 %
# 2019 10th, C.B.S.E Aggarsain Public School 94.60 %
# Internship
# • Game Development Internship (July, 2024) : Engineered a Clash Royale clone in Unity 3D utilizing C
# scripting for gameplay mechanics, multiplayer networking, and real-time synchronization. Applied Agile
# methodologies and used Git for version control to ensure smooth, collaborative development.
# PROJECTS
# • Face Recognition using openCV : Developed a real-time face recognition system using OpenCV, integrating
# Haar Cascades, HOG, deep learning, and LBPH for detection and classification. Optimized accuracy and
# performance with hyperparameter tuning and GPU acceleration.
# • AI-Powered CPU SchedulerWeb App : Built a React-based CPU scheduler with a Flask backend, integrating
# a machine learning model (85% accuracy) to predict optimal scheduling algorithms. Included ChatGPT
# API for interactive guidance and used dynamic charts to visualize soft metrics like fairness, turnaround
# time, and priority handling. Designed to support both technical analysis and user-friendly decision-making.
# • Banking Software : Developed a robust banking application in Java utilizing Swing for a sleek user interface.
# Integrated with MySQL for efficient data management, ensuring secure and seamless financial
# transactions.
# TECHNICAL SKILLS
# • Languages : Java (advanced), C++ (advanced), C (proficient), Javascript (proficient), HTML&CSS, Python
# .
# • Technologies : OpenCV , Unity 3D , NetCode for Game Objects , MySQL, Git , Swing, React, Flask,
# Linux .
# • Skills : Object Oriented Programming, Game Mechanics, Real Time Synchronisation, UI/UX Designing,
# Data Structures and Algortihms.
# CERTIFICATIONS
# • Successfully completed (NDE)v1 administered by EC Council
# • Attained (EHE)v1 certification administered by EC Council
# ACHIEVEMENTS
# • Finalist, Techgig Code Gladiators 2024 Hackathon.
# • Secured 313th rank in TCS CodeVita Season 12, a global coding competition.
# POSITIONS OF RESPONSIBILITY
# • Class Representative Class Representative (since July 2023): Spearheaded communication between students
# and faculty, leading efforts to address student concerns and facilitate effective issue resolution. ."""    
# tokenize_resume(text, None)