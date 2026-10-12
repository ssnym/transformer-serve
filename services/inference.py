import torch


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



def generate_text(prompt:str, tokenizer, model, device, system_prompt, 
                  max_new_tokens: int = 100, temperature: float = 0.6, do_sample: bool = True):

    text_in = build_input(prompt, tokenizer, model, system_prompt)
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
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