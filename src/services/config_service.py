from pydantic_settings import BaseSettings


class _ConfigService(BaseSettings):
    db_type: str = "remote"

    doc_url_path: str = "docs_url.json"

    access_status: str = "private"

    database_url: str = (
        "postgresql+asyncpg://admin:admin@2.tcp.eu.ngrok.io:19794/hrtist"
    )

    anthropic_api_key: str | None = None
    mistral_api_key: str | None = None
    

    class Config:
        env_file = ".env"
        extra = "ignore"


ConfigService = _ConfigService()
