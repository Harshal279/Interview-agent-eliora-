import json
import os
import re

from llm import get_openai_client

client = get_openai_client()
DEFAULT_MODEL = os.getenv("EVALUATOR_MODEL", "gemini-2.0-flash")


def _normalized_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _fallback_evaluation(generated_question: str, candidate_answer: str, grounded_answer: str) -> dict:
    cand = _normalized_text(candidate_answer)
    ground = _normalized_text(grounded_answer)

    overlap = 0
    if cand and ground:
        cand_tokens = set(cand.split())
        ground_tokens = set(ground.split())
        overlap = len(cand_tokens & ground_tokens) / max(1, len(ground_tokens))

    answer_length = len(candidate_answer.split())
    technical = round(min(10, max(0, overlap * 8 + (answer_length > 25) * 1.5)), 2)
    communication = round(min(10, max(0, 4 + min(4, answer_length / 20))), 2)
    problem_solving = round(min(10, max(0, technical * 0.6 + overlap * 3)), 2)
    confidence = round(min(10, max(0, communication * 0.6 + 2.2)), 2)
    relevance = round(min(10, max(0, overlap * 8 + 1.5)), 2)
    overall_score = round((technical + communication + problem_solving + confidence + relevance) / 5, 2)

    strengths = []
    weaknesses = []
    if overlap >= 0.2:
        strengths.append("Relevant technical content")
    else:
        weaknesses.append("Low grounding to the expected answer")

    if answer_length >= 20:
        strengths.append("Detailed explanation")
    else:
        weaknesses.append("Answer is too brief")

    if len(candidate_answer) > 0:
        strengths.append("Attempted a direct answer")

    return {
        "question": generated_question,
        "candidate_answer": candidate_answer,
        "scores": {
            "technical": technical,
            "communication": communication,
            "problem_solving": problem_solving,
            "confidence": confidence,
            "relevance": relevance,
        },
        "overall_score": overall_score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "feedback": "The answer was evaluated using a deterministic fallback heuristic because no live LLM score was available.",
        "difficulty": "medium",
        "topic": "general",
        "followup_topics": ["depth of explanation", "real-world usage"],
    }


def evaluator(generated_question: str, candidate_answer: str, grounded_answer: str):
    prompt = f"""
You are an expert AI Technical Interview Evaluator.

Question:
{generated_question}

Candidate Answer:
{candidate_answer}

Grounded answer:
{grounded_answer}

Evaluate the answer and return ONLY valid JSON with this schema:

{{
    "question": "{generated_question}",
    "candidate_answer": "{candidate_answer}",
    "scores": {{
        "technical": 0,
        "communication": 0,
        "problem_solving": 0,
        "confidence": 0,
        "relevance": 0
    }},
    "overall_score": 0,
    "strengths": [],
    "weaknesses": [],
    "feedback": "",
    "difficulty": "",
    "topic": "",
    "followup_topics": []
}}
"""

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI Interview Evaluator."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        payload = response.choices[0].message.content
        if payload:
            return json.loads(payload)
    except Exception:
        pass

    return _fallback_evaluation(generated_question, candidate_answer, grounded_answer)