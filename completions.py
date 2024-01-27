import logging
from llama_cpp import Llama
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown


def configure_model(selected_model, model_config, schema):
    model = Llama(
        model_path=f"/Users/pwilson/lollms/lollms-webui/models/gguf/{model_config['file']}",
        verbose=False,
        stream=True,
        n_gpu_layers=-1,
        n_ctx=0,
    )
    system_prompt_string = schema["system_prompt_string"]
    user_prompt_string = schema["user_prompt_string"]
    bot_prompt_string = schema["bot_prompt_string"]


def create_completion(model, messages, user_prompt_string):
    try:
        stream = model.create_completion(
            "".join(messages), stream=True, stop=[user_prompt_string], max_tokens=0
        )
        return stream
    except Exception as e:
        logging.error(f"Error during create_completion: {e}")
        return None


def render_response_stream(console, stream, selected_model):
    full_response = []
    with Live(
        Markdown(f"_{selected_model.title()} is thinking..._"),
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
