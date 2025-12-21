
"""
app/services/orchestrator.py

Orquestrador principal que coordena o fluxo simplificado.
Agora, ele apenas processa a mensagem do usuário e registra a conversa.
Comentários em português.
"""

from typing import Dict, Any
import logging

# Importa DB
from app.db.database import SessionLocal
from app.db.models import Conversation

logger = logging.getLogger(__name__)

def _log_conversation(db_session, user_input: str, assistant_output: str):
    """
    Persiste a conversa no banco de dados.
    Usa o modelo Conversation definido em app.db.models.
    """
    conv = Conversation(
        user_input=user_input,
        assistant_output=assistant_output
    )
    db_session.add(conv)
    db_session.commit()
    db_session.refresh(conv)
    return conv

async def handle_message(user_message: str) -> Dict[str, Any]:
    """
    Função principal do orquestrador simplificado.
    Recebe a mensagem do usuário e retorna uma resposta básica.
    """

    assistant_out = f"Received your message: '{user_message}'. Thank you!"

    # Persiste no banco (bloqueante, mas rápido). Abre uma sessão local.
    try:
        with SessionLocal() as db:
            _log_conversation(db, user_message, assistant_out)
    except Exception as e:
        # Não falhar completamente por conta do DB; apenas logar o erro.
        logger.exception("Failed to log conversation: %s", e)

    # Retorna o objeto resultado
    return {
        "assistant": assistant_out
    }
