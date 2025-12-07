from typing import Optional

from pydantic import EmailStr


class Settings:
    app_title: str = 'QRKot — благотворителный фонд помощи котам'
    app_description: str = (
        'Приложение для сбора пожертвовании на нужды котиков.'
    )
    app_version: str = '1.0.0'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    first_superuser_email: EmailStr = 'admin@example.com'
    first_superuser_password: str = 'admin123'

    email: Optional[EmailStr] = None

    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None


settings = Settings()
