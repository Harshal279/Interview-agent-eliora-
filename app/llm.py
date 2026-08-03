from openai import OpenAI
import os

def get_openai_client():
    return OpenAI(
        api_key="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",
        base_url="https://api.groq.com/openai/v1",
    )

