"""
Application settings.

Loads all environment variables from the .env file using
Pydantic Settings.

All configurable values should be defined here.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# class Settings(BaseSettings):
#     """
#     Application Configuration
#     """
#     APP_NAME:str = "Employee Management System"
#     API_VERSIOn:str= "v1"
#     DEBUG:bool  = True
#     HOST:str = "0.0.0.0"
#     PORT:int = 8000
#     model_config = SettingsConfigDict(
#         env_file  = "env",
#         case_sensitive =True,
#         extra = "ignore",
#     )

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    """
    Application configuration.
    """

    # ==========================================================
    # Application Configuration
    # ==========================================================

    APP_NAME: str

    API_VERSION: str

    DEBUG: bool = False

    HOST: str

    PORT: int

    # ==========================================================
    # Database Configuration
    # ==========================================================

    DB_HOST: str

    DB_PORT: int

    DB_NAME: str

    DB_USER: str

    DB_PASSWORD: str

    DATABASE_URL: str

    # ==========================================================
    # Pydantic Settings Configuration
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )
    
@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """
    return Settings()

settings =  get_settings()
