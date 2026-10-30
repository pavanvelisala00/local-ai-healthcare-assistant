"""Command-line entry point for the Local AI Healthcare Assistant."""

from guardrails import check_input, check_output
from model_loader import generate_response


def main() -> None:
    print("Local AI Healthcare Assistant (educational prototype)")
    print("Type 'exit' to quit. Do not use this tool for urgent medical needs.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        allowed, warning = check_input(question)
        if not allowed:
            print(f"Safety notice: {warning}\n")
            continue

        try:
            answer = generate_response(question)
        except (RuntimeError, OSError, ValueError) as exc:
            print(f"Model error: {exc}\n")
            continue

        safe, output_warning = check_output(answer)
        if not safe:
            print(f"Response withheld: {output_warning}\n")
        else:
            print(f"Assistant: {answer}\n")


if __name__ == "__main__":
    main()
