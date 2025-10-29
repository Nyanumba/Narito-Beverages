from pydantic_settings import BaseSettings
from typing import Any 

class Settings(BaseSettings):
 # Database
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: str
    database_url: str | None = None  # optional, in case you use a direct URL later

    # JWT / Auth
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Email configuration
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str
    
    model_config = {
         "env_file": ".env",
        "env_file_encoding": "utf-8"
    }
settings = Settings()
 