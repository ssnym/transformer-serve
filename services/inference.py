import torch
from threading import Thread
from transformers import TextIteratorStreamer


def build_input(prompt, tokenizer, model, system_prompt):
    # Instruct models with a chat template get a system + user  message
    if tokenizer.chat_template is not None:
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content":prompt},
        ]
        return tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
    # Base model or seq2seq get the raw input
    return prompt


def stream_text(prompt:str, tokenizer, model, device, system_prompt,
                max_new_tokens:int = 100, temperature: float = 0.2, do_sample: bool = True):
    text_in = build_input(prompt, tokenizer, model, system_prompt)
    inputs = tokenizer(text_in, return_tensors="pt", add_special_tokens=False).to(device)
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    gen_kwargs = {
        **inputs,
        "streamer": streamer,
        "max_new_tokens": max_new_tokens,
        "pad_token_id": tokenizer.eos_token_id,
        "do_sample": do_sample,
    }

    if do_sample:
        gen_kwargs.update(temperature=temperature, top_p=0.9)

    def run():
        try:
            with torch.no_grad():
                model.generate(**gen_kwargs)
        except Exception as e:
            streamer.text_queue.put(f"\n[error: {e}]")
            streamer.end()

    Thread(target=run, daemon=True).start()
    return streamer  # iterate over this to get text chunks
         


def generate_text(prompt:str, tokenizer, model, device, system_prompt, 
                  max_new_tokens: int = 100, temperature: float = 0.6, do_sample: bool = True):

    text_in = build_input(prompt, tokenizer, model, system_prompt)
    inputs = tokenizer(text_in, return_tensors="pt", add_special_tokens=False).to(device)
    gen_kwargs = {
        "max_new_tokens": max_new_tokens,
        "pad_token_id": tokenizer.eos_token_id,
        "do_sample": do_sample,
    }

    if do_sample:
            gen_kwargs.update(temperature=temperature, top_p = 0.9)

    with torch.no_grad():
        outputs = model.generate(
            **inputs, **gen_kwargs
        )
    
    # Causal models return prompt + answer; drop the prompt tokens.
    # Seq2seq models return only the answer.

    if model.config.is_encoder_decoder:
        new_tokens = outputs[0]
    else:
        new_tokens = outputs[0][inputs["input_ids"].shape[1]:]


    text = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    return text