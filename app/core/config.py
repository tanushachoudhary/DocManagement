from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Azure OpenAI
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str

    # Database
    DATABASE_URL: str

    # App
    ENV: str = "dev"

    class Config:
        env_file = ".env"
        extra = "ignore"  # 👈 IMPORTANT


def get_settings():
    return Settings()
