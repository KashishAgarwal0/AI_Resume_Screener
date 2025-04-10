import pdfplumber
import pytesseract
from PIL import Image
from docx import Document
from transformers import pipeline
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util


# Load NER pipeline
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)
model = SentenceTransformer('all-MiniLM-L6-v2')
# Define a simple skill list
SKILL_LIST = [
    "python", "java", "c++", "html", "css", "javascript", "react",
    "nodejs", "express", "sql", "mongodb", "machine learning", "deep learning",
    "flask", "django", "tensorflow", "pytorch", "git", "docker", "linux"
]

# Define basic project-related keywords
PROJECT_KEYWORDS = ["project", "developed", "created", "built", "designed"]

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# Clean subword tokens from Hugging Face NER
def clean_entities(raw_entities):
    merged = []
    buffer = ""
    for item in raw_entities:
        word = item["word"]
        if word.startswith("##"):
            buffer += word[2:]
        else:
            if buffer:
                merged.append(buffer)
            buffer = word
    if buffer:
        merged.append(buffer)

    # Fuzzy merging of near-duplicates
    final_entities = []
    for ent in merged:
        if not any(fuzz.ratio(ent, existing) > 85 for existing in final_entities):
            final_entities.append(ent)

    return list(set([w.strip() for w in final_entities if len(w) > 1]))

# Skill extractor (basic keyword match)
def extract_skills(text):
    text_lower = text.lower()
    found_skills = [skill for skill in SKILL_LIST if skill in text_lower]
    return list(set(found_skills))

# Project extractor (simple keyword-based)
def extract_projects(text):
    projects = []
    lines = text.split("\n")
    for line in lines:
        if any(keyword in line.lower() for keyword in PROJECT_KEYWORDS):
            projects.append(line.strip())
    return list(set(projects))

# Named Entity Recognition and Skill/Project Extraction
def extract_entities(text):
    entities = {
        "Skills": extract_skills(text),
        "Projects": extract_projects(text)
    }
    return entities

# Match resume to job description
def match_resume_to_jd(resume_data, job_description):
    jd_skills = extract_skills(job_description)
    resume_skills = set(resume_data.get("Skills", []))

    matched_skills = resume_skills.intersection(jd_skills)
    score = round(len(matched_skills) / len(jd_skills) * 100, 2) if jd_skills else 0

    return {
        "JD Skills": list(jd_skills),
        "Matched Skills": list(matched_skills),
        "Resume Match Score": f"{score}%"
    }

def compute_match_score(resume_text, jd_text):
    embeddings = model.encode([resume_text, jd_text], convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    return round(float(similarity.item()) * 100, 2)