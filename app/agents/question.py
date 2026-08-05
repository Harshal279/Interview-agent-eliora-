import os

from llm import get_openai_client

client = get_openai_client()
DEFAULT_MODEL = os.getenv("QUESTION_MODEL", "gemini-2.0-flash")


def _fallback_questions() -> list[str]:
    return [
        "Explain the most important technical skill mentioned in your resume and how you used it in practice.",
        "Walk me through a project you led or significantly contributed to, including the problem, approach, and outcome.",
        "Describe a time you debugged a complex issue and how you narrowed down the root cause.",
        "What is your experience with Python, APIs, and backend system design?",
        "How do you prioritize trade-offs between speed, quality, and maintainability in development?",
        "Tell me about a challenge you faced in a team setting and how you handled it.",
        "What are your strengths and how do they align with the role you are targeting?",
        "Why are you interested in this role, and what would success look like for you in the first few months?",
        "How do you approach learning a new technology or framework quickly?",
        "What metrics or evidence do you use to show that your work delivered real impact?",
    ]


def _parse_questions(raw_text: str | None) -> list[str]:
    if not raw_text:
        return _fallback_questions()

    lines = []
    for line in raw_text.splitlines():
        cleaned = line.strip().lstrip("-•*1234567890. ")
        if cleaned and cleaned.lower() not in {"resume", "intro"}:
            lines.append(cleaned)

    if lines:
        return lines[:15]

    return _fallback_questions()


def generate_interview_questions(resume: str):
    prompt = f"""
You are an expert technical interviewer.

Analyze the following resume and create a practical interview set.
Generate 15 concise interview questions in a clean numbered list.

Resume:
{resume}

Return only the questions, with no extra explanation.
"""

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
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
            temperature=0.5,
        )
        content = response.choices[0].message.content
        return _parse_questions(content)
    except Exception:
        return _fallback_questions()