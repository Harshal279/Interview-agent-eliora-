from urllib import response

from schedule import Job
from agents import memory
from services.resume import extract_text_from_pdf
from llm import get_openai_client

profile = memory.get_profile()

history = memory.get_history()

client = get_openai_client()

def generate_interview_questions(resume: str):

    prompt =f""" You are an AI Interviewer.

Candidate Profile:

{profile}

Interview History:

{history}

Generate the next interview question.

Rules:

1. Never repeat a previous question.

2. If the candidate has weaknesses, ask questions that test those areas.

3. If confidence is low, begin with a slightly easier question.

4. If technical score is consistently high (>8), gradually increase difficulty.

5. Prefer follow-up topics suggested by previous evaluations.

6. Avoid asking about already mastered topics unless verifying consistency.

Return only:

{
    "question": "...",
    "grounded answer to the question": "...",
    "difficulty": "...",
    "topic": "...",
    "reason": "..."
}
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


next_question = generate_interview_questions(

    profile=profile,

    history=history
)