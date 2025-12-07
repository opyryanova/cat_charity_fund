from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import AuthenticationBackend, \
    BearerTransport, JWTStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users.exceptions import InvalidPasswordException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.constants import PASSWORD_MIN_LENGTH, TOKEN_LIFE_CYCLE
from app.core.db import get_async_session
from app.core.logger import logger
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=TOKEN_LIFE_CYCLE,
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < PASSWORD_MIN_LENGTH:
            raise InvalidPasswordException(
                reason=(
                    f'Пароль должен содержать не менее '
                    f'{PASSWORD_MIN_LENGTH} символов'
                )
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не может содержать email'
            )

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        """Логирует факт успешной регистрации пользователя."""
        logger.info('Пользователь %s успешно зарегистрирован', user.email)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
