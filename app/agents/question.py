from schedule import Job

from services.resume import extract_text_from_pdf
from llm import get_openai_client

client = get_openai_client()

def generate_interview_questions(resume: str):

    prompt = f"""
You are an expert technical interviewer.

Analyze the following resume.

Generate:
- 10 technical questions
- 5 project-based questions
- 5 HR questions

Resume:
{resume}
intro :
{}
Return only the questions.
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {
                "role": "system",
                "content": "You are an AI Interviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5
    )

    return response.choices[0].message.content