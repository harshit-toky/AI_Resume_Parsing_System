import json
from resume_parser import ResumeParser
from resume_ranker import ResumeRanker


def main():
    # Initialize the parser and ranker
    parser = ResumeParser()
    ranker = ResumeRanker()

    # Sample resume text (in a real application, this would come from PDF/docx files)
    sample_resume1 = """
    John Doe
    john.doe@example.com
    (123) 456-7890
    linkedin.com/in/johndoe

    SUMMARY
    Experienced software engineer with 5+ years of experience in Python development and machine learning.

    SKILLS
    Python, Java, SQL, TensorFlow, PyTorch, Docker, Kubernetes, AWS, Machine Learning, Data Analysis

    EXPERIENCE
    Senior Software Engineer
    ABC Technologies, Inc.
    2018-2022
    - Developed machine learning models for customer segmentation
    - Led a team of 5 engineers in building a data pipeline
    - Implemented CI/CD processes using Jenkins and Docker

    Software Engineer
    XYZ Solutions
    2015-2018
    - Built RESTful APIs using Django and Flask
    - Worked on database optimization and query performance

    EDUCATION
    Master of Science in Computer Science
    Stanford University
    2013-2015

    Bachelor of Engineering in Computer Science
    MIT
    2009-2013
    """

    sample_resume2 = """
    Jane Smith
    jane.smith@example.com
    (987) 654-3210
    linkedin.com/in/janesmith

    SUMMARY
    Front-end developer with expertise in React and Angular.

    SKILLS
    JavaScript, HTML, CSS, React, Angular, Node.js, Git, Webpack, Responsive Design

    EXPERIENCE
    Front-end Developer
    Web Solutions Inc.
    2019-2022
    - Developed responsive web applications using React
    - Implemented state management with Redux
    - Collaborated with UX designers to create intuitive interfaces

    UI Developer
    Creative Designs
    2017-2019
    - Built interactive UI components using Angular
    - Created cross-browser compatible websites

    EDUCATION
    Bachelor of Science in Web Development
    University of California
    2013-2017
    """

    # Sample job description
    job_description = """
    We are looking for an experienced Software Engineer with strong Python skills and machine learning experience.
    The ideal candidate will have knowledge of TensorFlow, PyTorch, and experience with cloud platforms like AWS.
    Responsibilities include developing machine learning models, implementing data pipelines, and collaborating with data scientists.
    Requirements:
    - 3+ years of Python development
    - Experience with machine learning frameworks
    - Knowledge of Docker and Kubernetes
    - Good understanding of CI/CD practices
    """

    # Parse resumes
    parsed_resume1 = parser.parse_resume(sample_resume1)
    parsed_resume2 = parser.parse_resume(sample_resume2)

    # Convert from JSON string to dict for display
    resume1_dict = json.loads(parsed_resume1)
    resume2_dict = json.loads(parsed_resume2)

    print("Parsed Resume 1:")
    print(json.dumps(resume1_dict, indent=2))
    print("\nParsed Resume 2:")
    print(json.dumps(resume2_dict, indent=2))

    # Rank resumes
    ranked_resumes = ranker.rank_resumes(
        [parsed_resume1, parsed_resume2],
        job_description
    )

    print("\nRanked Resumes:")
    for i, ranked_resume in enumerate(ranked_resumes):
        print(f"\nRank {i + 1}:")
        print(f"Name: {ranked_resume['resume']['name']}")
        print(f"Similarity Score: {ranked_resume['similarity_score']:.4f}")
        print(f"Skills: {', '.join(ranked_resume['resume']['skills'])}")


if __name__ == "__main__":
    main()