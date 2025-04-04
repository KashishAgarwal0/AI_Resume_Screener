import pdfplumber
import pytesseract
from PIL import Image
from docx import Document

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# Function to extract named entities (Example)
def extract_entities(text):
    # Dummy implementation (Replace with actual NER model)
    return {"Name": ["John Doe"], "Organization": ["Google"], "Skills": ["Python", "ML"]}
