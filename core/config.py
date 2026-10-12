import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-0.5B-Instruct")
MODEL_TYPE = os.getenv("MODEL_TYPE", "causal") # "seq2seq" or "causal"

SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful assistant. Answer clearly and concisely.",
)