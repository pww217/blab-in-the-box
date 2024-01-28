import logging
from rich.console import Console

from source.io import (
    load_config,
    load_instructions,
    parse_model_config,
    gather_user_input,
)
from source.completions import (
    configure_model,
    create_completion,
    render_cli_response_stream,
)


logging.basicConfig(encoding="utf-8", level=logging.INFO)


def main():
    config_json = load_config("config.json")
    instructions = load_instructions("instructions.txt")
    model_config = parse_model_config(config_json)

    # Here we configurate and insantiate a model object
    model = configure_model(model_config)

    messages = [
        {"role": "system", "content": f"{instructions}"},
    ]

    console = Console()  # Initiate console stream
    console.clear()  # Clear console before chat start

    while True:
        try:
            user_input = gather_user_input()
            user_input = {"role": "user", "content": f"{user_input}"}
            messages.append(user_input)
            console.print()

            # Start the stream and retrieve response
            stream = create_completion(model, messages)
            full_response = render_cli_response_stream(
                console, stream, config_json["selected_model"]
            )
            # Append new response to history
            messages.append({"role": "assistant", "content": f"{full_response}"})

        except KeyboardInterrupt:
            print("\n[Received interrupt!]\n")
            continue

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            continue


if __name__ == "__main__":
    main()
