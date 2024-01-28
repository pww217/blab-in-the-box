import logging
from rich.console import Console

from source.io import load_config, load_instructions, parse_json, gather_user_input
from source.completions import (
    configure_model,
    create_completion,
    render_cli_response_stream,
)


logging.basicConfig(encoding="utf-8", level=logging.INFO)


def main():
    config_json = load_config("config.json")
    instructions = load_instructions("instructions.txt")
    (model_config, schema) = parse_json(config_json)
    # Here we configurate and insantiate a model object
    (
        model,
        system_prompt_string,
        user_prompt_string,
        bot_prompt_string,
    ) = configure_model(model_config, schema)

    # Assemble the initial system prompt
    # messages = [f"{system_prompt_string} {instructions}\n"]

    messages = [
        {"role": "system", "content": f"{instructions}"},
    ]

    console = Console()  # Initiate console stream
    console.clear()  # Clear console before chat start

    while True:
        try:
            user_input = gather_user_input()
            user_input = {"role": "user", "content": f"{user_input}"}
            console.print()
            messages.append(user_input)

            # Start the stream and retrieve response
            stream = create_completion(model, messages, user_prompt_string)
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
