from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agents.question import generate_interview_questions
from services.resume import extract_text_from_pdf

app = FastAPI(
    title="AI Interview Engine",
    description="Backend API for the AI Interview Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_questions(resume_text: str):
    return generate_interview_questions(resume_text)


@app.get("/")
async def root():

    resume_text = extract_text_from_pdf("resume.pdf")

    questions = generate_questions(resume_text)

    return {
        "questions": questions
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }