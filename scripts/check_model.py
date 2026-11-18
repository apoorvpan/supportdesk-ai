import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    """Verify configuration and make one small model request."""
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(project_root / ".env")

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    if not api_key:
        raise SystemExit(
            "Missing OPENAI_API_KEY. Add it to the project's .env file."
        )

    with OpenAI(
        api_key=api_key,
        timeout=30.0,
        max_retries=0,
    ) as client:
        response = client.responses.create(
            model=model,
            instructions=(
                "You are SupportDesk AI, a customer-support assistant. "
                "Keep your reply brief. "
                "Do not claim access to accounts or company documentation."
            ),
            input="Introduce yourself in one sentence.",
            max_output_tokens=150,
        )

    print("Model response:")
    print(response.output_text)

    if response.usage:
        print(f"\nInput tokens: {response.usage.input_tokens}")
        print(f"Output tokens: {response.usage.output_tokens}")


if __name__ == "__main__":
    main()