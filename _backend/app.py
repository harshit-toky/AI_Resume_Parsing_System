from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF for extracting text from PDFs

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
            return jsonify({"message": "PDF processed successfully", "extractedText": extracted_text})

    elif request.json and "resumeText" in request.json:  # If text is submitted
        resume_text = request.json["resumeText"]
        return jsonify({"message": "Text received successfully", "resumeText": resume_text})

    return jsonify({"error": "No valid data received"}), 400

if __name__ == "__main__":
    app.run(debug=True)
