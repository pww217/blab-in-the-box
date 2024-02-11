#!/bin/bash

# This script will set up the llama_cpp library to run on Apple ARM
# Other settings to make use of the GPU are in the config/python files.

# check the path of your xcode install 
# must install if not present
xcode-select -p

# if xcode is missing then install it... it takes ages;
xcode-select --install

wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh

conda create -n llama python=3.9.16
conda activate llama

pip uninstall llama-cpp-python -y
CMAKE_ARGS="-DLLAMA_METAL=on" pip install -U llama-cpp-python --no-cache-dir
pip install 'llama-cpp-python[server]'

pip install -r requirements.txt