import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carrega as variáveis do .env para o ambiente
load_dotenv()

class Settings(BaseSettings):
    AUTH_SERVER_URL: str = os.getenv("AUTH_SERVER_URL", "https://localhost:3002") # https://localhost:3002
    MENTORIA_SERVER_URL: str = os.getenv("MENTORIAS_SERVER_URL", "https://localhost:8000") # https://localhost:8000

    LOGIN_USER_URL: str = f"{AUTH_SERVER_URL}/auth/login"
    REGISTER_USER_URL: str = f"{AUTH_SERVER_URL}/auth/register"
    KEY_USER_URL: str = f"{AUTH_SERVER_URL}/auth/key"
    DELETE_USER_URL: str = f"{AUTH_SERVER_URL}/auth/delete"

settings = Settings()