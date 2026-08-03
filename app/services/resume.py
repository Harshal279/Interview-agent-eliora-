import pypdf 
from fastapi import APIRouter

def get_resume():
    return {
        "message": "Resume endpoint working"
    }

def upload_resume():
    return {
        "message": "Resume uploaded successfully"
    }

def extract_text_from_pdf(file_path: str):
    reader = pypdf.PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    print ("Extracted text from PDF:")
    return text
