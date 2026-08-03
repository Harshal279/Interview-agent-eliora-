from openai import OpenAI
import os

def get_openai_client():
    return OpenAI(
        api_key="",
        base_url="https://api.groq.com/openai/v1",
    )

