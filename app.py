from fastapi import FastAPI
from pydantic import BaseModel, Field
from core.model_loader import load_model
from services.inference import generate_text

app=FastAPI()

tokenizer, model, device = load_model()

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    max_new_tokens: int = Field(default=100, ge=1, le=512)
    temperature: float = Field(default=0.6, ge=0.0, le=2.0)
    do_sample: bool = False


@app.get("/")
def home():
    return{"message":"HF Spaces"}


@app.post("/generate")
def generate_post(request: GenerateRequest):
    text = generate_text(
        request.prompt, tokenizer, model, device,
        max_new_tokens=request.max_new_tokens,
        temperature=request.temperature,
        do_sample=request.do_sample
    )
    return {"output" : text}