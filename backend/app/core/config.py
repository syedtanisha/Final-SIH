import urllib.parse
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "MoSPI AI-Enabled Statistical Learning Platform"
    API_V1_STR: str = "/api/v1"
    
    # Exact database variables from .env
    DATABASE_USERNAME: Optional[str] = None
    DATABASE_PASSWORD: Optional[str] = None
    DATABASE_HOSTNAME: Optional[str] = None
    DATABASE_PORT: Optional[str] = "5432"
    DATABASE_NAME: Optional[str] = "postgres"
    DATABASE_URL_OVERRIDE: Optional[str] = None

    # Exact token expiration & security variables from .env
    ACCESS_EXPIRETIME_MINUTES: int = 60
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"

    # Exact AI provider variables from .env
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GROK_API_KEY: Optional[str] = None
    XAI_API_KEY: Optional[str] = None
    GROK_MODEL: str = "grok-2-latest"
    XAI_BASE_URL: str = "https://api.x.ai/v1"

    # Defaults for internal services
    AI_PROVIDER: str = "auto"
    LLM_MAX_RETRIES: int = 2
    LLM_TIMEOUT_SECONDS: float = 30.0
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"

    # iGOT Integration settings
    IGOT_API_BASE_URL: str = "https://igotkarmayogi.gov.in/api"
    IGOT_CLIENT_ID: Optional[str] = None
    IGOT_CLIENT_SECRET: Optional[str] = None
    IGOT_SANDBOX_MODE: bool = True

    # Voice Assistant (STT & TTS) settings
    OPENAI_API_KEY: Optional[str] = None
    VOICE_STT_PROVIDER: str = "auto"
    VOICE_TTS_PROVIDER: str = "auto"
    VOICE_DEFAULT_LANGUAGE: str = "en"

    model_config = SettingsConfigDict(

        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def DATABASE_URL(self) -> str:
        if self.DATABASE_URL_OVERRIDE:
            return self.DATABASE_URL_OVERRIDE
        if self.DATABASE_USERNAME and self.DATABASE_PASSWORD and self.DATABASE_HOSTNAME:
            encoded_password = urllib.parse.quote_plus(self.DATABASE_PASSWORD)
            return (
                f"postgresql://{self.DATABASE_USERNAME}:{encoded_password}@"
                f"{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT or '5432'}/"
                f"{self.DATABASE_NAME or 'postgres'}"
            )
        return "sqlite:///./statlearn.db"

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        return self.ACCESS_EXPIRETIME_MINUTES

settings = Settings()
