import streamlit as st
import docx2txt
import pdfminer.high_level
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Title
st.title("💼 Smart Resume Analyzer & Job Matcher")

# Upload resume
uploaded_file = st.file_uploader("Upload Your Resume (PDF or DOCX)", type=['pdf', 'docx'])

# Upload job description
jd_file = st.file_uploader("Upload Job Description (PDF, DOCX, or TXT)", type=['pdf', 'docx', 'txt'])

# Function to read file content
def extract_text(file):
    if file.name.endswith('.pdf'):
        return pdfminer.high_level.extract_text(file)
    elif file.name.endswith('.docx'):
        return docx2txt.process(file)
    elif file.name.endswith('.txt'):
        return file.read().decode("utf-8")
    return ""

# Function to extract skills
def extract_skills(text):
    skill_keywords = ["python", "java", "c++", "sql", "machine learning", "data science", "communication", "teamwork", "leadership", "html", "css", "javascript"]
    doc = nlp(text.lower())
    found_skills = set()
    for token in doc:
        if token.text in skill_keywords:
            found_skills.add(token.text)
    return list(found_skills)

# Function to calculate match score
def calculate_match_score(resume_text, jd_text):
    documents = [resume_text, jd_text]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)

# Run analysis
if uploaded_file is not None and jd_file is not None:
    resume_text = extract_text(uploaded_file)
    jd_text = extract_text(jd_file)

    st.subheader("📄 Resume Text:")
    st.write(resume_text[:1000] + "...")  # Truncate for display

    st.subheader("📃 Job Description Text:")
    st.write(jd_text[:1000] + "...")

    # Skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    st.subheader("🧠 Skills Found in Resume:")
    st.write(resume_skills)

    st.subheader("📌 Skills Required in JD:")
    st.write(jd_skills)

    # Match stats
    matched_skills = set(resume_skills).intersection(set(jd_skills))
    unmatched_skills = set(jd_skills) - set(resume_skills)

    st.subheader("📊 Skill Match Overview")
    st.metric("Matched Skills", len(matched_skills))
    st.metric("Missing Skills", len(unmatched_skills))

    st.bar_chart({
        "Skills": ["Matched", "Missing"],
        "Count": [len(matched_skills), len(unmatched_skills)]
    })

    # Match percentage
    score = calculate_match_score(resume_text, jd_text)
    st.subheader("📈 Overall Resume-JD Match Score")
    st.metric("Match %", f"{score}%")

    # Suggestions
    st.subheader("💡 Suggestions to Improve Your Resume")
    if unmatched_skills:
        st.warning("You may want to add the following skills to your resume:")
        st.write(unmatched_skills)
    else:
        st.success("Your resume covers all key skills in the job description!")
