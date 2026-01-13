from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    Inherits from Pydantic's BaseSettings for automatic validation.
    """
    
    # --- Azure OpenAI Credentials ---
    # These are required to authenticate with the Azure AI service
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str

    # --- Database Connection ---
    DATABASE_URL: str

    # --- Application State ---
    ENV: str = "dev"  # Defaults to 'dev' if not specified

    class Config:
        """
        Pydantic configuration class.
        """
        env_file = ".env"
        
        # 'extra = "ignore"' prevents the app from crashing if the .env file 
        # contains variables not defined in this class (e.g., system-level vars).
        extra = "ignore" 


def get_settings():
    """
    Factory function to create a cached instance of Settings.
    In a larger app, we would use @lru_cache here to prevent reading .env on every call.
    """
    return Settings()