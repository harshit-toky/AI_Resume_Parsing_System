from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import fitz  # PyMuPDF for extracting text from PDFs
from parsing import tokenize_resume
from calculate_similarity_score import analyze_resume
import json
import os
import shutil
from werkzeug.utils import secure_filename
from authenticity_checker import ResumeAuthenticityChecker

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")  # Open PDF from memory
    text = ""
    for page in pdf_document:
        text += page.get_text("text") + "\n"  # Extract text from each page
    return text.strip()

@app.route("/submit", methods=["POST"])
def submit():
    if "pdfFile" in request.files:  # If a file is submitted
        pdf_file = request.files["pdfFile"]
        if pdf_file.filename != "":
            extracted_text = extract_text_from_pdf(pdf_file)
            tokenize_resume(extracted_text, None)
            return jsonify({"message": "PDF processed successfully", "extractedText": extracted_text})

    elif request.json and "resumeText" in request.json:  # If text is submitted
        resume_text = request.json["resumeText"]
        tokenize_resume(resume_text, None)
        return jsonify({"message": "Text received successfully", "resumeText": resume_text})

    return jsonify({"error": "No valid data received"}), 400

@app.route("/get-parsed-resume", methods=["GET"])
def get_parsed_resume():
    """Serve the parsed JSON resume."""
    try:
        full_path = r"F:\React JS\ai_resume_parsing_system\_backend\resume_parsed_data.json"
        with open(full_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Parsed resume data not found"}), 404

@app.route("/download-tokenized-resume", methods=["GET"])
def download_tokenized_resume():
    """Allow users to download the tokenized resume file."""
    try:
        return send_file("./tokenized_resume.txt", as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "Tokenized resume file not found"}), 404

@app.route("/compare-resume", methods=["POST"])
def compare_resume():
    data = request.json

    if not data or "jobDescription" not in data:
        return jsonify({"error": "Job description is required"}), 400

    try:
        # Load parsed resume data
        with open("resume_parsed_data.json", "r", encoding="utf-8") as file:
            parsed_resume = json.load(file)

        job_description = data["jobDescription"]

        # Call analyze_resume function
        # matched_skills, unmatched_skills, matched_education, job_education, similarity_score = analyze_resume(parsed_resume, job_description)
        result = analyze_resume(parsed_resume, job_description)

        return jsonify({
            "matchedSkills": result["matchedSkills"],
            "unmatchedSkills": result["unmatchedSkills"],
            "similarityScore": float(result["similarityScore"])  # Ensure it's a float
        })


    except FileNotFoundError:
        print("Error")
        return jsonify({"error": "Parsed resume data not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
PARSED_FOLDER = 'parsed'
@app.route('/upload-resumes', methods=['POST'])
def upload_resumes():
    # Clear parsed folder
    if os.path.exists(PARSED_FOLDER):
        shutil.rmtree(PARSED_FOLDER)
    os.makedirs(PARSED_FOLDER, exist_ok=True)

    files = request.files
    if not files:
        return "No files uploaded", 400
    count = 0
    for key in files:
        file = files[key]
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1].lower()

        if file_ext not in ['.pdf']:
            return f"Unsupported file type: {file_ext}", 400

        # Convert PDF (or other) file-like to text
        text = extract_text_from_pdf(file)
        count += 1
        # Construct path where parsed JSON will be saved
        parsed_filename = filename.rsplit('.', 1)[0] + f'_{count}_parsed.json'
        print(parsed_filename)
        parsed_path = os.path.join(PARSED_FOLDER, parsed_filename)

        # Now call your parsing function with text and the target path
        tokenize_resume(text, parsed_path)

    return jsonify({"message": "Parsed data stored successfully."}), 200

@app.route("/compare-multiple-resumes", methods=["POST"])
def compare_multiple_resumes():
    data = request.json

    if not data or "jobDescription" not in data:
        return jsonify({"error": "Job description is required"}), 400

    job_description = data["jobDescription"]
    parsed_folder = "parsed"
    results = []

    # Loop through all .json files in the parsed folder
    for filename in os.listdir(parsed_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(parsed_folder, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                parsed_resume = json.load(file)

            result = analyze_resume(parsed_resume, job_description)

            results.append({
                "filename": filename,
                "matchedSkills": result["matchedSkills"],
                "unmatchedSkills": result["unmatchedSkills"],
                "similarityScore": float(result["similarityScore"])
            })

    return jsonify(results), 200

@app.route("/check-authenticity", methods=["POST"])
def check_authenticity():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    resume_file = request.files["resume"]
    text_data = extract_text_from_pdf(resume_file)
    
    # Save parsed tokens to JSON
    current_dir = os.getcwd()
    parsed_resume_path = os.path.join(current_dir, "_plag_checking.json")
    tokenize_resume(text_data, parsed_resume_path)

    # Read text data from the saved JSON
    try:
        with open(parsed_resume_path, "r", encoding="utf-8") as f:
            parsed_resume_data = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Failed to read parsed resume: {str(e)}"}), 500

    # Initialize checker
    obj_authenticity_checker = ResumeAuthenticityChecker()
    
    # Call the checker with parsed data
    result = obj_authenticity_checker.check_resume_authenticity(parsed_resume_data)
    print(result)
    # Return the actual result
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)
