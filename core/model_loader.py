import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
from core.config import MODEL_NAME, MODEL_TYPE

def load_model():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    if MODEL_TYPE == "seq2seq":
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)
    elif MODEL_TYPE == "causal":
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)
    else:
        raise ValueError(f"Unsupported MODEL_TYPE: {MODEL_TYPE}")
    
    return tokenizer, model, device
