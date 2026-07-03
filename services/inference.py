def generate_text(prompt:str, tokenizer, model, device,
                  max_new_tokens: int = 100,
                  temperature: float = 0.6,
                  do_sample: bool = False):

    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=do_sample
    )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text