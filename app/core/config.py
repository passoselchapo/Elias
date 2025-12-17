"""
app/core/config.py

Configurações centrais da aplicação, lendo variáveis de ambiente
e fornecendo valores padrão. Os comentários estão em português.
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """
    Classe de configuração que carrega settings de variáveis de ambiente
    ou usa valores padrão.
    """
    # Configurações do Banco de Dados PostgreSQL
    # Exemplo: postgresql+psycopg2://user:password@host:port/database_name
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://user:password@localhost:5432/elias_db"
    )

    # Chave da API OpenAI (opcional). Se não fornecida, o sistema usa o fallback local.
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY", None)

    # URL base da API OpenAI (opcional). Pode ser útil para proxies ou APIs compatíveis.
    OPENAI_API_BASE: str | None = os.getenv("OPENAI_API_BASE", None)

    # Modelo da OpenAI a ser usado (ex: gpt-4o-mini). Padrão para gpt-4o-mini.
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    # Chave da API Gemini (opcional). Se não fornecida, o sistema usa o fallback local.
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY", None)

    # Host para a aplicação FastAPI. Padrão para 127.0.0.1 (localhost).
    HOST: str = os.getenv("HOST", "127.0.0.1")

    # Porta para a aplicação FastAPI. Padrão para 8000.
    PORT: int = int(os.getenv("PORT", 8000))

# Instancia a configuração para ser importada em outros módulos
settings = Config()
