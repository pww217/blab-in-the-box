import logging
import argparse
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


def configure_parser():
    parser = argparse.ArgumentParser(
        description="CLI for interacting with an LLM chatbot."
    )
    parser.add_argument("--prompt", help="Initial prompt for the chatbot", type=str)
    parser.add_argument(
        "--file", help="File containing input for the chatbot", type=str
    )
    args = parser.parse_args()
    return args


def main():
    args = configure_parser()

    selected_model, model_config = load_config("config.json")
    instructions = load_instructions("instructions.txt")

    model = configure_model(model_config)
    messages = [{"role": "system", "content": f"{instructions}"}]
    interactive_mode = True

    if args.prompt:
        messages.append({"role": "user", "content": args.prompt})
        interactive_mode = False
    if args.file:
        try:
            with open(args.file, "r") as file:
                file_content = file.read()
            messages.append({"role": "user", "content": file_content})
            interactive_mode = False
        except FileNotFoundError:
            print(f"Error: The file '{args.file}' was not found.")
            return
    

    console = Console()
    if interactive_mode:
        console.clear()
        while True:
            try:
                user_input = {"role": "user", "content": f"{gather_user_input()}"}
                messages.append(user_input)
                import json
                print(json.dumps(messages, indent=2))
                print()

                stream = create_completion(model, messages)
                full_response = render_cli_response_stream(
                    console, stream, selected_model
                )
                # Append new response to history
                messages.append({"role": "assistant", "content": f"{full_response}"})

            except KeyboardInterrupt:
                continue

            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                continue
    else:
        stream = create_completion(model, messages)
        full_response = render_cli_response_stream(console, stream, selected_model)
        console.print(full_response)  # Output to standard out


if __name__ == "__main__":
    main()
