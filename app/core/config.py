from pydantic import EmailStr


class Settings:
    app_title: str = 'QRKot — благотворительный фонд помощи котам'
    app_description: str = (
        'Приложение для сбора пожертвовании на нужды котиков.'
    )
    app_version: str = '1.0.0'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    first_superuser_email: EmailStr = 'admin@example.com'
    first_superuser_password: str = 'admin123'

    email: EmailStr | None = None

    type: str | None = None
    project_id: str | None = None
    private_key_id: str | None = None
    private_key: str | None = None
    client_email: str | None = None
    client_id: str | None = None
    auth_uri: str | None = None
    token_uri: str | None = None
    auth_provider_x509_cert_url: str | None = None
    client_x509_cert_url: str | None = None


settings = Settings()
