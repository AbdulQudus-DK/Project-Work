from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr
from pathlib import Path

class Settings(BaseSettings):

    mongo_uri: str = Field(alias="MONGO_URI")
    azure_openai_key: SecretStr = Field(alias="AZURE_OPENAI_KEY")
    azure_openai_endpoint: str = Field(alias="AZURE_OPENAI_ENDPOINT")
    azure_deployment_chat: str = Field(alias="AZURE_DEPLOYMENT_CHAT", default="gpt-4o-mini")
    azure_deployment_embed: str = Field(alias="AZURE_DEPLOYMENT_EMBED", default="embedding-deploy")
    summary_timeout: int = Field(alias="SUMMARY_TIMEOUT", default=30)
    summary_retry_attempts: int = Field(alias="SUMMARY_RETRY_ATTEMPTS", default=3)
    summary_rate_limit_seconds: int = Field(alias="SUMMARY_RATE_LIMIT_SECONDS", default=20)
    max_feeds_per_source: int = Field(alias="MAX_FEEDS_PER_SOURCE", default=10)
    log_level: str = Field(alias="LOG_LEVEL", default="INFO")

    class Config:
        env_file = Path(__file__).resolve().parent / ".env"
        validate_by_name = True
