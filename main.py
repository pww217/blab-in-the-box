import logging
import json
from llama_cpp import Llama
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

logging.basicConfig(encoding="utf-8", level=logging.INFO)


def load_config(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def parse_json(config):
    model_config = config["models"][MODEL]
    schema = config["schemas"].get(model_config["schema"])
    return model_config, schema


def gather_user_input():
    user_input = input("~ User ~\n")
    if user_input.lower() in ["exit", "q", "quit"]:
        print("Goodbye!")
        exit()
    return user_input.strip()


def create_completion(model, messages, user_prompt_string):
    try:
        stream = model.create_completion(
            "".join(messages), stream=True, stop=[user_prompt_string], max_tokens=0
        )
        return stream
    except Exception as e:
        logging.error(f"Error during create_completion: {e}")
        return None


def render_response_stream(console, stream):
    full_response = []
    with Live(
        Markdown(f"_{MODEL.title()} is thinking..._"),
        console=console,
        auto_refresh=False,
    ) as live:
        console.print("~ Assistant ~")
        for segment in stream:
            text = segment["choices"][0]["text"]
            full_response.append(text)
            md = Markdown("".join(full_response))
            live.update(md, refresh=True)
    console.print()
    return "".join(full_response)


# Your chosen model, defined in config.json
MODEL = "zephyr"


def main():
    config_json = load_config("config.json")
    (model_config, schema) = parse_json(config_json)

    with open("instructions.txt") as f:
        instructions = f.read()

    model = Llama(
        model_path=f"models/{model_config['file']}",
        verbose=False,
        stream=True,
        n_gpu_layers=-1,
        n_ctx=0,
    )
    system_prompt_string = schema["system_prompt_string"]
    user_prompt_string = schema["user_prompt_string"]
    bot_prompt_string = schema["bot_prompt_string"]

    # Assemble the initial system prompt
    messages = [f"{system_prompt_string} {instructions}\n"]

    console = Console()  # Initiate console stream
    console.clear()  # Clear console before chat start

    while True:
        try:
            print("".join(messages))
            user_input = gather_user_input()
            full_prompt = f"{user_prompt_string} {user_input}\n{bot_prompt_string} "
            console.print()
            messages.append(full_prompt)

            # Start the stream and retrieve response
            stream = create_completion(model, messages, user_prompt_string)
            full_response = render_response_stream(console, stream)

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
