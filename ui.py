import streamlit as st
from app import parse_resume
import os

st.title("AI Resume Authenticity Checker")

uploaded_file = st.file_uploader("Upload a resume (PDF/DOCx)", type=["pdf", "docx"])

if uploaded_file:
    # Save uploaded file temporarily
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Parse and analyze resume
    gptzero_api_key = st.text_input("Enter GPTZero API Key (optional)", type="password")
    result = parse_resume(temp_path, gptzero_api_key)
    
    # Display results
    st.subheader("Parsed Resume Data")
    st.json(result["parsed_data"])
    
    st.subheader("Authenticity Analysis")
    authenticity = result["authenticity_result"]
    st.write(f"**Authenticity Score**: {authenticity['authenticity_score']}/100")
    st.write(f"**AI Content Score**: {authenticity['ai_score']:.2f}")
    st.write(f"**Suspected AI-Generated**: {authenticity['is_suspected_ai']}")
    st.write("**Flags**:")
    for flag in authenticity["authenticity_flags"]:
        st.write(f"- {flag}")
    
    # Clean up
    os.remove(temp_path)