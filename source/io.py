import json
from typing import Union, List, Dict, Tuple

def load_config(file_path: str) -> Tuple[str, Dict]:
    """
    Loads a configuration file at the specified path and returns the selected model and its
    configuration.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        tuple: A tuple containing the selected model name and its configuration.
    """
    with open(file_path, "r") as file:
        config = json.load(file)
    selected_model = config["selected_model"]
    model_config = config["models"][selected_model]
    return selected_model, model_config


def load_instructions(file_path: str) -> str:
    """
     Loads instructions from a file at the specified path and returns them as a string.

     Args:
         file_path (str): The path to the instructions file.

     Returns:
         str: The contents of the instructions file.
    """
    with open(file_path) as f:
        instructions = f.read()
    return instructions


def gather_user_input() -> Union[str, List[str]]:
    """
    Gathers user input and handles special cases like exit commands.

    Returns:
        str: The user's input, stripped of leading and trailing whitespace.
    """
    user_input = input(">> User\n")
    if user_input.lower() in ["exit", "q", "quit"]:
        print("Goodbye!")
        exit()
    elif user_input.lower() in ["file"]:
        filename = input(">> What is the file path?\n")
        prompt = input(">> What would you like to ask about it? (Optional)\n")
        contents = f"{prompt}:\n\n```{read_user_file(filename)}\n```"
        return contents
    else:
        return user_input.strip()


def read_user_file(filename: str) -> str:
    """
    Reads the content of a file specified by the user and returns it as a string.

    Args:
        filename (str): The path to the user-specified file.

    Returns:
        str: The contents of the user-specified file.
    """
    with open(filename, "r") as f:
        return f.read()
