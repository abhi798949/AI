from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Manually set pad token id to eos token id (50256) if not set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_text(prompt, max_length=50, temperature=0.7, top_k=50, top_p=0.95):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)  # padding=True sets attention mask
    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,  # pass attention mask explicitly
        max_length=max_length,
        do_sample=True,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        pad_token_id=tokenizer.pad_token_id,  # explicitly set pad token id for generation
        num_return_sequences=1
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

prompt = "what is AI"
generated = generate_text(prompt)
print("Prompt:", prompt)
print("Generated Text:", generated)
