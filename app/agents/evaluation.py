import json
from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url="https://api.groq.com/openai/v1"
)


def evaluator(generated_question: str, candidate_answer: str):

    prompt = f"""
You are an expert AI Technical Interview Evaluator.

Question:
{generated_question}

Candidate Answer:
{candidate_answer}

Evaluate the answer.

Return ONLY valid JSON with this schema:

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

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Groq-supported model
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
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)

    return result


evaluation = evaluator(
    "Define what is RAG?",
    "Um, okay. So, RAG... uh, RAG stands for Retrieval-Augmented Generation. And, basically, what it does is... sorry, let me rephrase. It’s a framework used to improve the accuracy of LLMs.So, instead of just relying on the model's internal weights—you know, what it learned during pre-training—it, um, it actually hooks up the LLM to an external database. Like, a vector database.Uh, how it actually works step-by-step is... well, there are three main parts. First is the retrieval phase. When a user asks a question—the query—the system converts that text into an embedding. Um, using an embedding model. Then it does a similarity search... wait, sorry, a semantic search inside the vector database to find chunks of text that match the user's intent.Then comes the... the augmentation part. This is where the system takes those retrieved chunks—the context—and sort of glues them together with the original user prompt. It creates a new, bigger prompt.And finally, the... the generation phase. The LLM reads this whole combined prompt—so it’s basically like an open-book exam for the AI—and it generates an answer based only on that specific data.Um, as for why you’d use it over fine-tuning... wow, my mind just went blank for a second, sorry. Right, fine-tuning. Fine-tuning actually changes the model's weights, which is super expensive and takes a long time. Plus, if your data changes every day, you can't keep fine-tuning it. RAG is way better for dynamic data because you just update the database, not the whole model. And... um, yeah, it also really helps stop hallucinations because the model is forced to stick to the facts you give it. I think... yeah, I think that covers the main points."
)

print(json.dumps(evaluation, indent=4))