from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'QRKot — благотворительный фонд помощи котам'
    app_description: str = (
        'Приложение для сбора пожертвований на нужды котиков.'
    )
    app_version: str = '1.0.0'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    first_superuser_email: EmailStr = 'admin@example.com'
    first_superuser_password: str = 'admin123'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
