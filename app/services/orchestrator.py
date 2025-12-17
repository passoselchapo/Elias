"""
app/services/orchestrator.py

Orquestrador principal que coordena o fluxo:
 - pontua importância (scorer)
 - gera sumário (summarizer)
 - obtém resposta da persona (personas + OpenAI)
 - persiste a conversa no banco (db)
Comentários em português.
"""

from typing import Optional, Dict, Any
import os
import logging

# Importa componentes do core
from app.core import config
from app.core import scorer
from app.core import summarizer

# Importa DB
from app.db.database import SessionLocal
from app.db.models import Conversation

# Dependência opcional: openai (usada em summarizer / respostas)
try:
    import openai
except Exception:
    openai = None

logger = logging.getLogger(__name__)


def _get_openai_client():
    """Retorna o cliente openai configurado ou None."""
    api_key = config.OPENAI_API_KEY
    if not api_key:
        return None
    if openai:
        openai.api_key = api_key
        if config.OPENAI_API_BASE:
            openai.api_base = config.OPENAI_API_BASE
        return openai
    return None


def heuristic_importance(text: str) -> float:
    """
    Wrapper para o scorer. Mantido para conveniência de import externo.
    Retorna um float entre 0.0 e 1.0
    """
    return scorer.heuristic_importance(text)


async def summarize_text(text: str) -> str:
    """
    Usa o summarizer do core para gerar um resumo.
    Pode ser LLM-backed ou fallback local.
    """
    return await summarizer.summarize_text(text)


async def ask_persona_response(persona_name: str, user_message: str) -> str:
    """
    Gera resposta da persona. Usa o prompt do persona + OpenAI se disponível.
    Se API key ausente, retorna fallback simulado.
    """
    persona = personas_module.get_persona(persona_name) or personas_module.get_persona("fullstack")
    system_prompt = persona.get("system_prompt", "")
    max_tokens = persona.get("config", {}).get("max_tokens", 600)

    openai_client = _get_openai_client()
    if not openai_client:
        # Fallback simulado para desenvolvimento offline
        return f"[SIMULATED RESPONSE - persona={persona_name}] {user_message[:400]}"

    # Segurança: envolvemos a chamada em try/except
    try:
        resp = openai_client.ChatCompletion.create(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        # A resposta real normalmente está aqui:
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.exception("OpenAI request failed: %s", e)
        return f"[ERROR: OpenAI request failed] {str(e)}"


def _log_conversation(db_session, user_input: str, assistant_output: str, importance: float, summary: str):
    """
    Persiste a conversa no banco de dados.
    Usa o modelo Conversation definido em app.db.models.
    """
    conv = Conversation(
        user_input=user_input,
        assistant_output=assistant_output,
        importance_score=importance,
        summary=summary,
        persona=persona
    )
    db_session.add(conv)
    db_session.commit()
    db_session.refresh(conv)
    return conv


async def handle_message(user_message: str, persona: str = "fullstack") -> Dict[str, Any]:
    """
    Função principal do orquestrador.
    Recebe a mensagem do usuário e o nome da persona.
    Retorna um dicionário com:
      - assistant: texto da resposta
      - importance: score (0.0 - 1.0)
      - summary: resumo da mensagem do usuário
      - persona: persona usada
    """

    # 1) Calcula importância (rápido, síncrono)
    importance = heuristic_importance(user_message)

    # 2) Gera resumo (assíncrono - LLM ou fallback)
    summary = await summarize_text(user_message)

    # 3) Gera resposta da persona (pode chamar OpenAI)
    assistant_out = await ask_persona_response(persona, user_message)

    # 4) Persiste no banco (bloqueante, mas rápido). Abre uma sessão local.
    try:
        with SessionLocal() as db:
            _log_conversation(db, user_message, assistant_out, importance, summary, persona)
    except Exception as e:
        # Não falhar completamente por conta do DB; apenas logar o erro.
        logger.exception("Failed to log conversation: %s", e)

    # 5) Retorna o objeto resultado
    return {
        "assistant": assistant_out,
        "importance": importance,
        "summary": summary,
        "persona": persona
    }
