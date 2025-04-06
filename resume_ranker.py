import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResumeRanker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def preprocess_resume(self, resume_data):
        """
        Convert parsed resume data to a single text string for TF-IDF processing.
        """
        # Convert resume data from JSON to dict if it's a string
        if isinstance(resume_data, str):
            resume_data = json.loads(resume_data)

        # Concatenate relevant fields into a single text
        text_data = []

        # Add skills (most important)
        if 'skills' in resume_data:
            text_data.extend([skill.lower() + ' ' + skill.lower() for skill in resume_data['skills']])

        # Add education details
        if 'education' in resume_data:
            for edu in resume_data['education']:
                text_data.append(edu.get('degree', '').lower())
                text_data.append(edu.get('institution', '').lower())

        # Add experience details
        if 'experience' in resume_data:
            for exp in resume_data['experience']:
                text_data.append(exp.get('job_title', '').lower())
                text_data.append(exp.get('company', '').lower())
                text_data.append(exp.get('description', '').lower())

        return ' '.join(text_data)

    def preprocess_job_description(self, job_description):
        """
        Preprocess job description for TF-IDF processing.
        """
        # Simple preprocessing: lowercase
        return job_description.lower()

    def compute_similarity(self, resume_text, job_text):
        """
        Compute similarity between resume and job description using TF-IDF and cosine similarity.
        """
        # Combine texts for vectorization
        texts = [resume_text, job_text]

        # Calculate TF-IDF vectors
        tfidf_matrix = self.vectorizer.fit_transform(texts)

        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

        return similarity

    def rank_resumes(self, resumes, job_description):
        """
        Rank resumes based on their similarity to the job description.

        Args:
            resumes: List of parsed resume data (JSON strings or dictionaries)
            job_description: String containing the job description

        Returns:
            List of dictionaries with resume data and similarity scores, sorted by score
        """
        # Preprocess job description
        job_text = self.preprocess_job_description(job_description)

        # Calculate similarity for each resume
        ranked_resumes = []

        for resume in resumes:
            # Convert resume to dict if it's a JSON string
            if isinstance(resume, str):
                resume_dict = json.loads(resume)
            else:
                resume_dict = resume

            # Preprocess resume
            resume_text = self.preprocess_resume(resume_dict)

            # Calculate similarity
            similarity = self.compute_similarity(resume_text, job_text)

            # Add to ranked list
            ranked_resumes.append({
                'resume': resume_dict,
                'similarity_score': similarity
            })

        # Sort by similarity score in descending order
        ranked_resumes.sort(key=lambda x: x['similarity_score'], reverse=True)

        return ranked_resumes