from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class InputModel(BaseModel):
    input: str


@app.post("/api/completion")
async def process(input_model: InputModel):
    user_input = input_model.input
    # Process the input asynchronously
    # For example, call your async model here
    processed_response = f"{user_input}"
    return {"response": processed_response}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
