import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from resume_extractor import extract_text_from_pdf, extract_entities  # Importing from extract.py
from docx import Document
from PIL import Image
import pytesseract

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "jpg", "png", "jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Named Entity Recognition (NER) model
ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# Load Sentence Transformer model for resume matching
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')

def allowed_file(filename):
    """Check if uploaded file is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_docx(docx_path):
    """Extract text from DOCX files"""
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_with_ocr(image_path):
    """Extract text from images using OCR"""
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def calculate_similarity(job_desc, resume_text):
    """Calculate similarity between job description and resume text"""
    job_embedding = similarity_model.encode(job_desc, convert_to_tensor=True)
    resume_embedding = similarity_model.encode(resume_text, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(job_embedding, resume_embedding)
    return similarity.item()

@app.route("/")
def index():
    """Render homepage"""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle resume upload, extract data, and compute match score"""
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    job_desc = request.form.get("job_description", "")

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Extract text based on file type
        if filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(filepath)  # Using extract.py function
        elif filename.endswith(".docx"):
            extracted_text = extract_text_from_docx(filepath)
        elif filename.endswith((".jpg", ".png", ".jpeg")):
            extracted_text = extract_text_with_ocr(filepath)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        # Perform Named Entity Recognition (NER)
        resume_info = extract_entities(extracted_text)  # Using extract.py function

        # Compute Resume Matching Score
        similarity_score = calculate_similarity(job_desc, extracted_text) if job_desc else None

        return jsonify({
            "Extracted Information": resume_info,
            "Resume Match Score": f"{similarity_score:.2f}" if similarity_score is not None else "No job description provided"
        })

    return jsonify({"error": "Invalid file type. Please upload a PDF, DOCX, or Image file."}), 400

if __name__ == "__main__":
    app.run(debug=True)
