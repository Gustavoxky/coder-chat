import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# Nome do modelo DeepSeek-Coder 6.7B
MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-instruct"
HF_AUTH_TOKEN = os.getenv("HF_AUTH_TOKEN")

# Configuração de quantização (otimizado para RTX 4050)
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,  # Melhor para RTX 4050
    bnb_4bit_use_double_quant=False,
)

# Carregar o tokenizador
print("Carregando o tokenizador...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HF_AUTH_TOKEN)

# Configurar pad_token_id (evita erro na geração)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

# Carregar o modelo com quantização otimizada
print("Carregando o modelo DeepSeek-Coder 6.7B...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=quantization_config,
    device_map="auto",  # Distribui automaticamente na GPU/CPU
    token=HF_AUTH_TOKEN,
)

def generate_response(prompt, max_length=256, temperature=0.7):
    """
    Gera uma resposta com base no prompt fornecido.
    """
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length,
        ).to(device)

        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            do_sample=True,  # Torna as respostas mais variadas
            temperature=temperature,
            pad_token_id=tokenizer.pad_token_id,
        )

        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar resposta: {e}")
