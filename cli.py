import logging
from rich.console import Console

from source.io import (
    load_config,
    load_instructions,
    gather_user_input,
)
from source.completions import (
    configure_model,
    create_completion,
    render_cli_response_stream,
)


logging.basicConfig(encoding="utf-8", level=logging.INFO)


def main():
    """
    The main function that runs the chatbot application.

    Loads configuration and instructions, sets up the model, and enters a loop to interact with
    the user.

    Returns:
        None
    """
    selected_model, model_config = load_config("config.json")
    instructions = load_instructions("instructions.txt")

    model = configure_model(model_config)
    messages = [{"role": "system", "content": f"{instructions}"}]

    console = Console()
    console.clear()
    while True:
        try:
            user_input = {"role": "user", "content": f"{gather_user_input()}"}
            messages.append(user_input)

            # import json
            # print(json.dumps(messages, indent=2))
            print()

            stream = create_completion(model, messages)
            full_response = render_cli_response_stream(console, stream, selected_model)
            # Append new response to history
            messages.append({"role": "assistant", "content": f"{full_response}"})

        except KeyboardInterrupt:
            print("\n[Received Interrupt!]\n")
            continue

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            continue


if __name__ == "__main__":
    main()
