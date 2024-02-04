import logging
from typing import Union, List, Dict, Tuple
from llama_cpp import Llama
from rich.live import Live
from rich.markdown import Markdown


def configure_model(model_config: Dict) -> Llama:
    """
    Configure the Llama model with the given configuration.

    Args:
        model_config (dict): A dictionary containing the model configuration.

    Returns:
        Llama: The configured Llama model instance.
    """
    model = Llama(
        model_path=f"/Users/pwilson/lollms/lollms-webui/models/gguf/{model_config['file']}",
        chat_format=model_config["chat_format"],
        verbose=False,
        stream=True,
        n_gpu_layers=-1,
        n_ctx=0,
    )
    return model


def create_completion(model: Llama, messages: List) -> Union[str, None]:
    """
    Create a chat completion using the given model and messages.

    Args:
        model (Llama): The configured Llama model instance.
        messages (list): A list of messages to be used for creating the completion.

    Returns:
        str or None: The completed message, or None if an error occurs during creation.
    """
    try:
        stream = model.create_chat_completion(messages, stream=True, max_tokens=0)
        print(type(stream))
        return stream
    except Exception as e:
        logging.error(f"Error during create_completion: {e}")
        return None


def render_cli_response_stream(console, stream: Union[str, List], selected_model: str) -> str:
    """
    Render the chat completion stream in the console.

    Args:
        console (rich.console.Console): The rich console instance.
        stream (str or list): The chat completion stream to be rendered.
        selected_model (Llama): The selected Llama model instance.

    Returns:
        str: The completed message as a string.
    """
    try:
        full_response = []
        with Live(
            Markdown(f"_{selected_model.title()} is thinking..._"),
            console=console,
            auto_refresh=False,
        ) as live:
            console.print(">> Assistant")
            for segment in stream:
                text = segment["choices"][0]["delta"].get("content")
                if text != None:
                    full_response.append(text)
                    md = Markdown("".join(full_response))
                    live.update(md, refresh=True)
        console.print()
        return "".join(full_response)
    except KeyboardInterrupt:
        print("\n[Received interrupt!]\n")
        # Here we still manage to append the partial response for context
        return "".join(full_response)
