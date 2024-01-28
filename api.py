from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from source.completions import configure_model, create_completion

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Input(BaseModel):
    input: str


class Response(BaseModel):
    response: str


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Render an HTML template with request data
    return templates.TemplateResponse(
        "index.html", {"request": request, "message": "Hello World"}
    )


@app.post("/api/completions", response_model=Response)
async def process(input_model: Input):
    user_input = input_model.input
    processed_response = f"Processed: {user_input}"
    return Response(response=processed_response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
