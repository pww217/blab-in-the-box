# Blab-in-the-box Documentation

## Overview

Blab-in-the-box is designed to offer an interactive chat experience powered by local OSS LLMs. This chatbot integrates with the command line interface and provides markdown rendering capabilities.

It supports GGUF formatted files from HuggingFace and elsewhere.

It is context-aware, storing the previous history into memory for use.

## Installation on Apple ARM (with GPU support)

This section outlines the steps to set up the chatbot on Apple ARM architecture, ii including the steps to enable GPU support. If you're running on an Apple ARM (M1/M2) processor and wish to utilize GPU capabilities, follow these instructions closely. The setup process is streamlined through a Bash script included in the repository, which automates the installation and configuration process.

For small to medium models, 16GB of RAM is necessary. For larger models (13b+) and lower loss models benefit from more memory and may not run.

### Prerequisites

- An Apple ARM (M1/M2) processor for GPU support.
- Xcode Command Line Tools installed on your macOS. The setup script will check for this and prompt installation if needed, but installing Xcode Command Line Tools can take some time.

### Step-by-Step Installation

1. Create a new virtual environment with venv or conda

```shell
python3 -m venv venv
source venv/bin/activate
```

2. Run `./setup-macos-metal.sh`

## Configuration

Here is a example configuration block:

```json
{
  "selected_model": "dolphin",
  "models": {
    "dolphin": {
      "file": "path/to/your/model/file",
      "chat_format": "chatml"
    },
    // Add other models here
  }
}
```

## instructions.txt

If you create an `instructions.txt` file as a regular text file and include some instructons of a system prompt, that will be ingested before any other inputs and act as a foundation for the conversation.

## Usage

After starting the chatbot, you can interact with it directly from the command line. The chatbot supports loading text from files, including PDFs, to provide context for the conversation.

Run either `make run` or `python cli.py` to start the interactive CLI.

To exit the chatbot, type `exit`, `q`, or `quit`.
To read from a file, type `/file`, then follow the prompts to provide the file path and optional prompt.
