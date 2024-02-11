import json
from typing import Union, List, Dict, Tuple
from PyPDF2 import PdfReader


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
    try:
        with open(file_path) as f:
            instructions = f.read()
            print("Loaded instructions.txt!")
            return instructions
    except:
        print("Failed to find an instructions.txt file.")


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


def read_pdf(filename: str) -> str:
    """
    Reads the content of a PDF file specified by the user and returns it as a string.

    Args:
        filename (str): The path to the user-specified PDF file.

    Returns:
        str: The contents of the user-specified PDF file.
    """
    pdf = PdfReader(filename)
    pages = pdf.pages
    pdf_contents = ""
    for i in pages:
        i = i.extract_text()
        pdf_contents += i
    contents = pdf_contents.replace("\n", " ")
    return contents


def gather_user_input() -> Union[str, List[str]]:
    """
    Gathers user input and handles special cases like exit commands.
    Converts files to plaintext strings and appends the prompt above.

    Returns:
        str: The user's input, stripped of leading and trailing whitespace.
    """
    user_input = input(">> User\n")
    if user_input.lower() in ["exit", "q", "quit"]:
        print("Goodbye!")
        exit()
    elif user_input.lower() in ["/file"]:
        filename = input(">> What is the text file path?\n").strip()
        prompt = input(">> What would you like to ask about it? (Optional)\n")
        if filename.split(".")[-1] == "pdf":
            contents = f"{prompt}:\n\n{read_pdf(filename)}\n"
        else:  # Any other regular text file
            contents = f"{prompt}:\n\n{read_user_file(filename)}\n"
        return contents

    else:
        return user_input.strip()
