
"""
app/core/summarizer.py

Este módulo lida com a lógica de sumarização de texto.
Pode usar um LLM (como OpenAI, Gemini) ou fornecer um fallback local.
Os comentários estão em português.
"""

import logging
from typing import Optional

from app.core import config

# Dependência opcional: google-generativeai
try:
    import google.generativeai as genai
except Exception:
    genai = None
    logging.warning("Módulo 'google-generativeai' não pode ser importado. Sumarização via Gemini será desativada.")

# Dependência opcional: openai
try:
    import openai
except Exception:
    openai = None
    logging.warning("Módulo 'openai' não pode ser importado. Sumarização via OpenAI será desativada.")


logger = logging.getLogger(__name__)

def _get_openai_client():
    '''
    Retorna o cliente openai configurado ou None.
    Reutiliza a chave de API e base da configuração global.
    '''
    api_key = config.OPENAI_API_KEY
    if not api_key:
        logger.debug("OPENAI_API_KEY não configurada. Sumarização usará outro LLM ou fallback local.")
        return None
    if openai:
        # Configura as credenciais globalmente para o módulo openai (versões < 1.x)
        # O orchestrator.py usa esta abordagem, então a replicamos aqui.
        openai.api_key = api_key
        if config.OPENAI_API_BASE:
            openai.api_base = config.OPENAI_API_BASE
        return openai
    # Se openai não foi importado com sucesso
    logger.debug("Módulo 'openai' não disponível. Sumarização usará outro LLM ou fallback local.")
    return None

def _get_gemini_client():
    '''
    Retorna o cliente Gemini configurado ou None.
    Reutiliza a chave de API da configuração global.
    '''
    api_key = config.GEMINI_API_KEY
    if not api_key:
        logger.debug("GEMINI_API_KEY não configurada. Sumarização usará outro LLM ou fallback local.")
        return None
    if genai:
        genai.configure(api_key=api_key)
        return genai
    logger.debug("Módulo 'google-generativeai' não disponível. Sumarização usará outro LLM ou fallback local.")
    return None


async def summarize_text(text: str) -> str:
    '''
    Gera um resumo do texto fornecido.
    Usa Gemini se a chave de API estiver configurada; caso contrário,
    tenta OpenAI, e finalmente fornece um fallback local simulado.
    '''
    gemini_client = _get_gemini_client()
    if gemini_client:
        try:
            logger.info("Tentando gerar resumo via Gemini para o texto: '%s'", text[:50])
            model = gemini_client.GenerativeModel('gemini-pro')
            response = model.generate_content(f'''Por favor, resuma o seguinte texto: {text}''')
            summary = response.text.strip()
            logger.info("Resumo gerado via Gemini com sucesso.")
            return summary
        except Exception as e:
            logger.error("Falha na requisição Gemini para sumarização: %s", e)

    openai_client = _get_openai_client()
    if openai_client:
        try:
            logger.info("Tentando gerar resumo via OpenAI para o texto: '%s'", text[:50])
            resp = openai_client.ChatCompletion.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "Você é um assistente de IA que resume textos de forma concisa e clara. Seu objetivo é extrair as informações mais importantes e apresentá-las em um formato resumido, mantendo o contexto principal."},
                    {"role": "user", "content": f'''Por favor, resuma o seguinte texto:

{text}'''} 
                ],
                max_tokens=150,
                temperature=0.3,
            )
            summary = resp["choices"][0]["message"]["content"].strip()
            logger.info("Resumo gerado via OpenAI com sucesso.")
            return summary
        except Exception as e:
            logger.error("Falha na requisição OpenAI para sumarização: %s", e)

    logger.info("Usando fallback de sumarização local para o texto: '%s'", text[:50])
    return f"[RESUMO SIMULADO] Este é um resumo do texto: '{text[:100]}...' (o restante foi omitido devido ao modo offline ou falta de API key)."
