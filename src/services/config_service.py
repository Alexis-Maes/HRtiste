from pydantic_settings import BaseSettings


class _ConfigService(BaseSettings):
    db_type: str = "remote"
    db_user: str = "postgres"
    db_name: str = "postgres"
    db_host: str = "localhost"
    db_port: int = 5432
    db_password: str = "postgres"

    doc_url_path: str = "docs_url.json"

    access_status: str = "private"

    database_url: str = (
        "postgresql+asyncpg://admin:admin@localhost:5432/profile_manager"
    )

    anthropic_api_key: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


ConfigService = _ConfigService()
