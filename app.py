import os
from pyresparser import ResumeParser
from authenticity_checker import ResumeAuthenticityChecker
import json

def parse_resume(file_path: str, gptzero_api_key: str = None) -> dict:
    """
    Parse a resume and check its authenticity.
    """
    # Initialize parsers
    parser = ResumeParser(file_path)
    authenticity_checker = ResumeAuthenticityChecker(gptzero_api_key)

    # Parse resume
    parsed_data = parser.get_extracted_data()
    
    # Add raw text to parsed data (assuming resume text is accessible)
    with open(file_path, 'rb') as f:
        # This is a placeholder; actual text extraction depends on file type
        parsed_data["raw_text"] = f.read().decode('utf-8', errors='ignore')

    # Check authenticity
    authenticity_result = authenticity_checker.check_resume_authenticity(parsed_data)
    
    # Combine results
    result = {
        "parsed_data": parsed_data,
        "authenticity_result": authenticity_result
    }
    
    return result

def main():
    resume_path = "path/to/resume.pdf"  # Replace with actual path
    gptzero_api_key = os.getenv("GPTZERO_API_KEY")  # Set in environment variables
    result = parse_resume(resume_path, gptzero_api_key)
    
    # Save results to JSON
    with open("resume_analysis.json", "w") as f:
        json.dump(result, f, indent=4)
    
    print("Resume analysis complete. Results saved to resume_analysis.json")

if __name__ == "__main__":
    main()