import spacy
from syntaxAnalysis import parse_resume

nlp = spacy.load("en_core_web_sm")

def tokenize_resume(text):
    doc = nlp(text)
    tokens = [token.text for token in doc]
    save_tokens_to_file(tokens)
    parse_resume(tokens)
    return tokens

def save_tokens_to_file(tokens, filename="tokenized_resume.txt"):
    """Save tokenized resume data in a structured format with double quotes and commas."""
    with open(filename, "w", encoding="utf-8") as file:
        formatted_tokens = ", ".join(f'"{token}"' for token in tokens)  # Enclose each token in double quotes
        file.write(formatted_tokens)
    print(f"✅ Tokenized data saved to {filename}")
