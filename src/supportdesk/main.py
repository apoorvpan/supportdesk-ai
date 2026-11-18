from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)

from model import create_client, get_response


def main() -> None:
    """Run the interactive support console."""
    try:
        client = create_client()
    except ValueError as error:
        print(f"Configuration error: {error}")
        return

    print("SupportDesk AI")
    print("Each question is independent for now.")
    print("Type 'exit' to quit.\n")

    with client:
        while True:
            try:
                message = input("You: ").strip()

                if message.lower() == "exit":
                    print("Goodbye!")
                    break

                if not message:
                    print("Please enter a question.\n")
                    continue

                print("\nThinking...")
                response = get_response(client, message)
                print(f"SupportDesk: {response}\n")

            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break

            except AuthenticationError:
                print("Authentication failed. Check your API key.\n")
                break

            except RateLimitError:
                print(
                    "Request limit or API quota reached. "
                    "Check your account usage and billing before retrying.\n"
                )

            except APITimeoutError:
                print("The request timed out. Please try again.\n")

            except APIConnectionError:
                print(
                    "Could not connect to the API. "
                    "Check your internet connection.\n"
                )

            except APIStatusError as error:
                print(
                    f"The API returned HTTP {error.status_code}. "
                    "Check the service status or request configuration.\n"
                )


if __name__ == "__main__":
    main()