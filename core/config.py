import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "google/flan-t5-small")
MODEL_TYPE = os.getenv("MODEL_TYPE", "seq2seq") # "seq2seq" or "causal"

