import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


INSTRUCTIONS = """
You are SupportDesk AI, a customer-support assistant.
Give clear, concise, helpful answers.
Ask a clarifying question when essential information is missing.
You do not yet have access to company documentation or customer accounts.
Do not invent company policies or claim you performed actions.
Never ask users to share passwords or API keys.
"""


def create_client() -> OpenAI:
    """Load configuration and create a reusable API client."""
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "Missing OPENAI_API_KEY. Add it to the project's .env file."
        )

    return OpenAI(timeout=30.0, max_retries=0)


def get_response(client: OpenAI, message: str) -> str:
    """Send one message to the model and return its text response."""
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions=INSTRUCTIONS,
        input=message,
        max_output_tokens=300,
    )

    return response.output_text.strip() or (
        "No text response was returned. Please try again."
    )