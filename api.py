from asyncio import sleep
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from source.io import load_config, load_instructions
from source.completions import configure_model, create_completion

""""
Doesn't work, may pick up again at some point.
"""

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Input(BaseModel):
    input: str


class Response(BaseModel):
    response: str


selected_model, model_config = load_config("config.json")
instructions = load_instructions("instructions.txt")
# Here we configurate and insantiate a model object
(
    model,
    system_prompt_string,
    user_prompt_string,
    bot_prompt_string,
) = configure_model(model_config)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Render an HTML template with request data
    return templates.TemplateResponse(
        "index.html", {"request": request, "message": "Hello World"}
    )


messages = [f"{system_prompt_string} {instructions}\n"]


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    full_response = []
    while True:
        user_input = await websocket.receive_text()
        full_prompt = f"{user_prompt_string} {user_input}\n{bot_prompt_string} "
        messages.append(full_prompt)
        stream = create_completion(model, messages, user_prompt_string)
        for segment in stream:
            text = segment["choices"][0]["text"]
            print(text, end="")
            # md = Markdown(text)
            await websocket.send_text(text)
            await sleep(0.1)
            # return text
        messages.append(f"{full_response}\n")  # Append new response to history


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
