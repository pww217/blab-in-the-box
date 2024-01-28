import json


def load_config(file_path):
    with open(file_path, "r") as file:
        config = json.load(file)
    return config


def load_instructions(file_path):
    with open("instructions.txt") as f:
        instructions = f.read()
    return instructions


def parse_json(config):
    selected_model = config["selected_model"]
    model_config = config["models"][selected_model]
    schema = config["schemas"].get(model_config["schema"])
    return model_config, schema


def gather_user_input():
    user_input = input("~ User ~\n")
    if user_input.lower() in ["exit", "q", "quit"]:
        print("Goodbye!")
        exit()
    return user_input.strip()
