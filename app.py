import torch
import time
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from core.model_loader import load_model
from core.config import MODEL_TYPE
from services.inference import generate_text

START_TIME = time.time()

app=FastAPI()

tokenizer, model, device = load_model()

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    max_new_tokens: int = Field(default=100, ge=1, le=512)
    temperature: float = Field(default=0.6, ge=0.0, le=2.0)
    do_sample: bool = False


@app.get("/")
def root(request: Request):
    scheme = request.headers.get("x-forwarded-proto", request.url.scheme)
    base_url = f"{scheme}://{request.url.netloc}"
    return {
        "message": "HF Transformer Serve — Causal + Seq2Seq inference API",
        "model": "Qwen/Qwen2.5-1.5B-Instruct",
        "generate_endpoint": f"{base_url}/generate (POST)",
        "health_check": f"{base_url}/health",
        "docs": "https://github.com/ssnym/transformer-serve — see README for a ready-to-copy curl example"
    }


@app.post("/generate")
def generate_post(request: GenerateRequest):
    text = generate_text(
        request.prompt, tokenizer, model, device,
        max_new_tokens=request.max_new_tokens,
        temperature=request.temperature,
        do_sample=request.do_sample
    )
    return {"output" : text}

@app.get("/health")
def health():
    return {
        "status" : "OK",
        "uptime_seconds" : round(time.time() - START_TIME, 2),
        "device" : str(device),
        "device_type" : "gpu" if torch.cuda.is_available() else "cpu",
        "model_name" : model.config._name_or_path,
        "model_type" : model.config.model_type,
        "num_parameters" : sum(p.numel() for p in model.parameters()),
        "configured_model_type" : MODEL_TYPE

    }