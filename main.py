import json
from authenticity_checker import ResumeAuthenticityChecker

def load_resume(file_path: str) -> dict:
    """
    Load the resume JSON file.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    # File path for the JSON resume
    resume_file = "/content/resume_parsed_data (1).json"
    
    # Load resume data
    try:
        resume_data = load_resume(resume_file)
    except FileNotFoundError:
        print("Error: JSON file not found. Please upload 'resume_parsed_data (1).json' to Colab.")
        return
    
    # Initialize authenticity checker
    checker = ResumeAuthenticityChecker()
    
    # Check authenticity
    authenticity_result = checker.check_resume_authenticity(resume_data)
    
    # Print results
    print("Resume Authenticity Analysis:")
    print(f"Authenticity Score: {authenticity_result['authenticity_score']}/100")
    print(f"AI Content Score: {authenticity_result['ai_score']:.2f}")
    print(f"Suspected AI-Generated: {authenticity_result['is_suspected_ai']}")
    if authenticity_result['triggered_buzzwords']:
        print(f"Triggered Buzzwords: {', '.join(authenticity_result['triggered_buzzwords'])}")
    print("Flags:")
    for flag in authenticity_result['authenticity_flags']:
        print(f"- {flag}")
    
    # Save results to JSON
    result = {
        "parsed_resume": resume_data,
        "authenticity_result": authenticity_result
    }
    with open("/content/resume_analysis.json", "w") as f:
        json.dump(result, f, indent=4)
    print("\nResults saved to /content/resume_analysis.json")

if __name__ == "__main__":
    main()