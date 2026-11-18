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


def get_response(
    client: OpenAI,
    history: list[dict[str, str]],
    message: str,
) -> str:
    """Generate a reply and remember the exchange after success."""
    user_message = {"role": "user", "content": message}
    request_messages = history + [user_message]

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions=INSTRUCTIONS,
        input=request_messages,
        max_output_tokens=300,
    )

    answer = response.output_text.strip()

    if not answer:
        return "No text response was returned. Please try again."

    history.extend(
        [
            user_message,
            {"role": "assistant", "content": answer},
        ]
    )

    # Retain the most recent 10 complete exchanges.
    del history[:-20]

    return answer