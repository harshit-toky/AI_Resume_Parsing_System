from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import fitz  # PyMuPDF for extracting text from PDFs
from parsing import tokenize_resume
from calculate_similarity_score import analyze_resume
import json

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
            tokenize_resume(extracted_text)
            return jsonify({"message": "PDF processed successfully", "extractedText": extracted_text})

    elif request.json and "resumeText" in request.json:  # If text is submitted
        resume_text = request.json["resumeText"]
        tokenize_resume(resume_text)
        return jsonify({"message": "Text received successfully", "resumeText": resume_text})

    return jsonify({"error": "No valid data received"}), 400

@app.route("/get-parsed-resume", methods=["GET"])
def get_parsed_resume():
    """Serve the parsed JSON resume."""
    try:
        with open("resume_parsed_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Parsed resume data not found"}), 404

@app.route("/download-tokenized-resume", methods=["GET"])
def download_tokenized_resume():
    """Allow users to download the tokenized resume file."""
    try:
        return send_file("../tokenized_resume.txt", as_attachment=True)
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

if __name__ == "__main__":
    app.run(debug=True)
