"""
app/cli.py

Este módulo fornece uma interface de linha de comando (CLI) para interagir
com o assistente, utilizando o orquestrador para processar as mensagens.
Os comentários estão em português.
"""

import asyncio
import argparse
import logging

# Importa o orquestrador que contém a lógica de negócio principal
from app.services import orchestrator

# Configuração básica de logging para o CLI
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main(message: str):
    """
    Função principal assíncrona para processar a mensagem via CLI.
    Chama o orquestrador e exibe a resposta.
    """
    logger.info("Recebida mensagem para a persona '%s': '%s'", persona, message)
    try:
        response_data = await orchestrator.handle_message(
            user_message=message,
            persona=persona
        )
        print("
--- Resposta do Assistente ---")
        print(f"Persona utilizada: {response_data['persona']}")
        print(f"Importância (0.0-1.0): {response_data['importance']:.2f}")
        print(f"Resumo da sua mensagem: {response_data['summary']}")
        print(f"Resposta do assistente: {response_data['assistant']}")
        print("----------------------------")
    except Exception as e:
        logger.error("Erro ao processar a mensagem: %s", e)
        print(f"Erro: Não foi possível processar a sua solicitação. Detalhes: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI para interagir com o Elias Assistant."
    )
    parser.add_argument(
        "message",
        type=str,
        help="A mensagem para enviar ao assistente."
    )
    
    args = parser.parse_args()

    # Executa a função assíncrona principal
        asyncio.run(main(args.message))
