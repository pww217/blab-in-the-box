import json


def load_config(file_path):
    with open(file_path, "r") as file:
        config = json.load(file)
    selected_model = config["selected_model"]
    model_config = config["models"][selected_model]
    return selected_model, model_config


def load_instructions(file_path):
    with open(file_path) as f:
        instructions = f.read()
    return instructions


def gather_user_input():
    user_input = input(">> User\n")
    if user_input.lower() in ["exit", "q", "quit"]:
        print("Goodbye!")
        exit()
    elif user_input.lower() in ["file"]:
        filename = input(">> What is the file name?\n")
        prompt = input(">> What would you like to ask about it? (Optional)\n")
        contents = f"{prompt}:\n\n```{read_user_file(filename)}\n```"
        return contents
    else:
        return user_input.strip()


def read_user_file(filename):
    with open(filename, "r") as f:
        return f.read()
