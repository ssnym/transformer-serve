import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-1.5B-Instruct")
MODEL_TYPE = os.getenv("MODEL_TYPE", "causal") # "seq2seq" or "causal"

