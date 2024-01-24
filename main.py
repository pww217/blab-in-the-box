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


def parse_json(model_config):
    model_file = model_config.get("file")
    system_prompt_string = model_config.get("system_prompt_string")
    user_prompt_string = model_config.get("user_prompt_string")
    bot_prompt_string = model_config.get("bot_prompt_string")
    return model_file, system_prompt_string, user_prompt_string, bot_prompt_string


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
    with Live(Markdown("_Thinking..._"), console=console, auto_refresh=False) as live:
        console.print("~ Assistant ~")
        for segment in stream:
            text = segment["choices"][0]["text"]
            full_response.append(text)
            md = Markdown("".join(full_response))
            live.update(md, refresh=True)
    console.print()
    return "".join(full_response)


# Your chosen model, defined in config.json
MODEL = "neuralbeagle"


def main():
    model_config = load_config("config.json")["models"][MODEL]
    (
        model_file,
        system_prompt_string,
        user_prompt_string,
        bot_prompt_string,
    ) = parse_json(model_config)

    with open("instructions.txt") as f:
        instructions = f.read()

    model = Llama(
        model_path=f"models/{model_file}",
        verbose=False,
        stream=True,
        n_gpu_layers=-1,
        n_ctx=0,
    )

    # Assemble the initial system prompt
    messages = [f"{system_prompt_string}{instructions}\n"]

    console = Console()  # Initiate console stream
    console.clear()  # Clear console before chat start

    while True:
        try:
            user_input = gather_user_input()
            full_prompt = f"{user_prompt_string}\n{user_input}\n{bot_prompt_string}"
            console.print()
            messages.append(full_prompt)

            # Start the stream and retrieve response
            stream = create_completion(model, messages, user_prompt_string)
            full_response = render_response_stream(console, stream)

            messages.append(f"{full_response}\n")  # Append new response to history
            
            # Writes to a file, although for now just as a debug tool
            with open("chat.log", "a") as f:
                f.write(f"{full_prompt}{full_response}")
        
        except KeyboardInterrupt:
            print("\nOutput interrupted!\n")
            continue



if __name__ == "__main__":
    main()
