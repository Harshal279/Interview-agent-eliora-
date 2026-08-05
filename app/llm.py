import os

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - handled by package installation
    def load_dotenv() -> bool:
        return False

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - handled by package installation
    OpenAI = None

load_dotenv()


def get_openai_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return None

    return OpenAI(
        api_key=api_key,
        base_url=os.getenv("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"),
    )

