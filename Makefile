setup:
	pip install -r requirements.txt

install-llama:
	CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 llm install llama-cpp-python
	llm install llm-llama-cpp