def get_response(message: str) -> str:
    """Return a placeholder response until the AI model is connected."""
    return (
        f"You asked: {message}\n"
        "The AI model is not connected yet."
    )


def main() -> None:
    """Run the interactive support console."""
    print("SupportDesk AI")
    print("Type a question, or type 'exit' to quit.\n")

    while True:
        try:
            message = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if message.lower() == "exit":
            print("Goodbye!")
            break

        if not message:
            print("Please enter a question.\n")
            continue

        response = get_response(message)
        print(f"\nSupportDesk: {response}\n")


if __name__ == "__main__":
    main()