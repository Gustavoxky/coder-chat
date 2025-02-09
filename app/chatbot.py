import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-instruct"
HF_AUTH_TOKEN = os.getenv("HF_AUTH_TOKEN")

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=False,
)

print("Carregando o tokenizador...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HF_AUTH_TOKEN)

if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

print("Carregando o modelo DeepSeek-Coder 6.7B...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=quantization_config,
    device_map="auto",
    token=HF_AUTH_TOKEN,
)

def generate_response(prompt, max_length=512, temperature=0.6, top_k=50, top_p=0.9, repetition_penalty=1.1):
    """
    Gera uma resposta otimizada e formatada corretamente.
    """
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"

        system_prompt = (
            "Você é um assistente altamente treinado para geração de código e explicações técnicas. "
            "Forneça respostas bem formatadas usando títulos, listas e códigos bem estruturados. "
            "Use markdown para melhor legibilidade."
        )

        full_prompt = f"{system_prompt}\n\nUsuário: {prompt}\n\n### Resposta ###\n"

        inputs = tokenizer(
            full_prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length,
        ).to(device)

        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            do_sample=True,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            pad_token_id=tokenizer.pad_token_id,
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        response = response.split("### Resposta ###")[-1].strip()

        response = response.replace("``` python", "```python")
        response = response.replace("\n\n", "\n")

        return response

    except Exception as e:
        raise RuntimeError(f"Erro ao gerar resposta: {e}")
