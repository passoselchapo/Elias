
"""
app/api.py

Este módulo define os endpoints da API FastAPI para o assistente.
Ele atua como uma camada fina, delegando a lógica principal ao orquestrador.
Os comentários estão em português.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Importa o orquestrador que contém a lógica de negócio principal
from app.services import orchestrator

# Cria a instância da aplicação FastAPI
app = FastAPI(
    title="Elias Assistant API",
    description="Backend minimalista para o assistente Elias, com foco em modularidade.",
    version="0.1.0",
)

# Define o modelo Pydantic para a requisição de chat
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest) -> Dict[str, Any]:
    """
    Endpoint principal para interagir com o assistente.
    Recebe uma mensagem do usuário e retorna a resposta do assistente.
    """
    try:
        # Delega a lógica de tratamento da mensagem ao orquestrador, apenas com a mensagem
        response_data = await orchestrator.handle_message(
            user_message=request.message
        )
        return response_data
    except Exception as e:
        # Captura exceções e retorna um erro HTTP 500
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Endpoint de verificação de saúde da API.
    Retorna uma mensagem simples para indicar que a API está funcionando.
    """
    return {"status": "ok", "message": "API do Elias Assistant está saudável!"}
