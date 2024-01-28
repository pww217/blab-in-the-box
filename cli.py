import logging
from rich.console import Console
from source.io import load_config, load_instructions, parse_json, gather_user_input
from source.completions import configure_model, create_completion, render_response_stream


logging.basicConfig(encoding="utf-8", level=logging.INFO)


def main():
    selected_model = "guanaco"

    config_json = load_config("config.json")
    instructions = load_instructions("instructions.txt")

    (model_config, schema) = parse_json(config_json, selected_model)
    (
        model,
        system_prompt_string,
        user_prompt_string,
        bot_prompt_string,
    ) = configure_model(selected_model, model_config, schema)

    # Assemble the initial system prompt
    messages = [f"{system_prompt_string} {instructions}\n"]

    console = Console()  # Initiate console stream
    console.clear()  # Clear console before chat start

    while True:
        try:
            # print("".join(messages))
            user_input = gather_user_input()
            full_prompt = f"{user_prompt_string} {user_input}\n{bot_prompt_string} "
            console.print()
            messages.append(full_prompt)

            # Start the stream and retrieve response
            stream = create_completion(model, messages, user_prompt_string)
            full_response = render_response_stream(console, stream, selected_model)

            messages.append(f"{full_response}\n")  # Append new response to history

        except KeyboardInterrupt:
            messages.append(f"{full_response}\n")
            print("\n[Received interrupt!]\n")
            continue

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            continue


if __name__ == "__main__":
    main()
