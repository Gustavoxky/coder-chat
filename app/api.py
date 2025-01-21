from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.chatbot import generate_response

app = FastAPI()

# Modelo de entrada da API
class ChatInput(BaseModel):
    prompt: str
    max_length: int = 128
    temperature: float = 0.7

@app.post("/chat")
async def chat(input: ChatInput):
    """
    Endpoint para gerar uma resposta com base no prompt fornecido.
    """
    try:
        response = generate_response(
            prompt=input.prompt,
            max_length=input.max_length,
            temperature=input.temperature,
        )
        return {"response": response}
    except Exception as e:
        print(f"Erro no processamento: {e}")  # Log no console
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")
