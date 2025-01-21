import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

MODEL_NAME = "mistralai/Mistral-7B-v0.3"
HF_AUTH_TOKEN = os.getenv("HF_AUTH_TOKEN")

# Configuração de quantização
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=False,
)

# Carregar o tokenizador
print("Carregando o tokenizador...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=HF_AUTH_TOKEN)

# Configurar pad_token_id
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

# Carregar o modelo com quantização
print("Carregando o modelo...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=quantization_config,
    device_map="auto",
    use_auth_token=HF_AUTH_TOKEN,
)

def generate_response(prompt, max_length=128, temperature=0.7):
    """
    Gera uma resposta com base no prompt fornecido.
    """
    try:
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length,
        ).to("cuda" if torch.cuda.is_available() else "cpu")

        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            do_sample=False,  # Determinístico para melhorar o tempo
            temperature=temperature,
            pad_token_id=tokenizer.pad_token_id,
        )

        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar resposta: {e}")
