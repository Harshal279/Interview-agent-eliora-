from agents import memory
from llm import get_openai_client

client = get_openai_client()

profile = memory.get_profile()
history = memory.get_history()


def evaluate_interview_questions(profile: str, history: str):

    prompt = f"""
You are an experienced AI Interview Evaluator.

Your task is to evaluate a candidate based on their profile and previous interview history, then generate the next interview question.

========================
CANDIDATE PROFILE
========================

{profile}

========================
INTERVIEW HISTORY
========================

{history}

=========================================================
STEP 1 - ORGANIZE THE CANDIDATE INFORMATION
=========================================================

Extract and summarize the following information if available.

Personal Information
- Name
- Current Role
- Years of Experience
- Education
- Certifications

Technical Skills
- Programming Languages
- Frameworks
- Databases
- Cloud Platforms
- AI/ML Skills
- Tools

Projects
For each project identify:
- Project Name
- Technologies Used
- Candidate's Responsibilities
- Challenges
- Achievements

Work Experience
For each company identify:
- Company
- Role
- Responsibilities
- Key Contributions

Strengths

Weaknesses

Missing Information

=========================================================
STEP 2 - REVIEW INTERVIEW HISTORY
=========================================================

Analyze previous interview conversations.

Identify:

- Questions already asked
- Candidate's answers
- Correct answers
- Incorrect answers
- Topics already covered
- Topics not yet covered
- Frequently weak areas
- Confidence level
- Communication quality
- Technical depth

Never ask the same question twice.

=========================================================
STEP 3 - SELECT THE NEXT QUESTION
=========================================================

Choose ONE interview question.

Priority:

1. Test weak areas first.
2. Ask project-based questions.
3. Ask experience-based questions.
4. Ask technical questions.
5. Ask behavioral questions.
6. Ask problem-solving questions.

The question should

- Not repeat previous questions
- Match candidate experience
- Increase difficulty gradually
- Be realistic for an actual interview

=========================================================
STEP 4 - DEFINE EVALUATION RUBRIC
=========================================================

Provide scoring criteria for the next answer.

Evaluate on:

Technical Accuracy (0-10)

Depth of Knowledge (0-10)

Problem Solving (0-10)

Communication (0-10)

Confidence (0-10)

Overall Score (0-50)

Rating

45-50 = Excellent
35-44 = Good
25-34 = Average
15-24 = Weak
0-14 = Poor

=========================================================
STEP 5 - OUTPUT FORMAT
=========================================================

Return ONLY valid JSON.

{{
    "candidate_summary": {{
        "strengths": [],
        "weaknesses": [],
        "missing_information": []
    }},
    "history_analysis": {{
        "questions_asked": [],
        "topics_completed": [],
        "topics_remaining": [],
        "confidence": ""
    }},
    "next_question": {{
        "category": "",
        "difficulty": "",
        "question": "",
        "reason": ""
    }},
    "evaluation_rubric": {{
        "technical_accuracy": "0-10",
        "depth_of_knowledge": "0-10",
        "problem_solving": "0-10",
        "communication": "0-10",
        "confidence": "0-10",
        "overall": "0-50"
    }}
}}

Return JSON only.
"""

    try:
        response = client.chat.completions.create(
            model="qwen/qwen3.6-27b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI Interview Evaluator."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            response_format={"type": "json_object"}
        )

        return response.choices[0].message.content

    except Exception as e:
        return {"error": str(e)}