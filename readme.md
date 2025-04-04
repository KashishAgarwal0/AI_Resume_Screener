The goal of this project is to automate resume screening by extracting key details from resumes and ranking candidates based on job descriptions. This will help recruiters save time by filtering out the best candidates automatically.

--------------------------------------------------------------------------------------------------------------------

Project Workflow
The project follows these steps:

Resume Upload → Users upload resumes in PDF or DOCX format.

Extracting Information → The system extracts key details like:

Name

Organizations (Work Experience & Education)

Skills

Other relevant details (optional, e.g., experience, projects, contact info, etc.)

Storing and Displaying Extracted Data → The extracted information is displayed on a website.

Matching Against Job Description (Next Step) → The system will compare resume data with a given job description and compute a match score.

Ranking Candidates → Candidates will be ranked based on relevance to the job description.

--------------------------------------------------------------------------------------------------------------------

Step-by-Step Guide to how this project is working :

1. Resume Upload
What Happens?

Users upload resumes (PDF/DOCX).

Backend processes the file for text extraction.

How to Do It?

Use Flask (Python backend) to handle file uploads.

Store resumes in a temporary directory for processing.

Use frontend (React) to allow users to upload files.

2. Extracting Information from Resumes
What Happens?

Extract text from resumes.

Identify important sections: Name, Organizations, Skills, etc.

How to Do It?

Use Python Libraries for extraction:

PyMuPDF or pdfminer.six → Extract text from PDFs

python-docx → Extract text from DOCX

Use Named Entity Recognition (NER) with spaCy to extract names, organizations, and skills.

Predefine a skills dictionary to match against extracted text.

Problem in Your Extracted Data:
Your current extraction has fragmented entities (e.g., "##gar", "##wal" instead of "Agarwal"). This happens due to improper tokenization.
✅ Fix: Improve spaCy model training or use a custom model with Hugging Face Transformers for better name/entity recognition.

3. Storing & Displaying Extracted Data
What Happens?

Extracted data is displayed on a website.

How to Do It?

Use React frontend to show extracted details in a structured format.

Store extracted data in a MongoDB / PostgreSQL database (optional for later ranking).

4. Matching Resume with Job Description (Next Step)
What Happens?

Compare extracted skills & experience with job requirements.

Compute a match score based on relevance.

How to Do It?

Convert job descriptions & resumes into numerical vectors using TF-IDF or Word Embeddings (BERT, SBERT, or T5 models).

Use cosine similarity or ML classification models to compute a match score.

Display a ranking system.

5. Ranking Candidates (Final Step)
What Happens?

Candidates are ranked based on their match score.

Recruiters see the best candidates first.

How to Do It?

Use a sorting algorithm based on the computed scores.

Display ranked candidates in a React dashboard.

--------------------------------------------------------------------------------------------------------------------


used pdfplumber → To extract text from PDFs.
python-docx → To extract text from DOCX files.

Extract key skills and experience from the resume.
Compare it with the job description to calculate a similarity score.
Rank candidates based on their match percentage.

We'll use spaCy for NLP and scikit-learn for similarity measurement.

we  are using transformers instead of spacy


 Integrate Named Entity Recognition (NER) with Transformers
Now that you’ve extracted text, let's use Hugging Face’s Transformers library to analyze resumes and extract names, organizations, skills, etc..