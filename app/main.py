from fastapi import FastAPI

from app.api.endpoints import charity_project, donation
from app.core.constants import CommonMessages
from app.core.db import Base, engine
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate


app = FastAPI(
    title=CommonMessages.APP_TITLE,
    description=CommonMessages.APP_DESCRIPTION,
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc',
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)

app.include_router(
    charity_project.router,
    prefix='/charity_project',
    tags=['charity_projects'],
)
app.include_router(
    donation.router,
    prefix='/donation',
    tags=['donations'],
)


@app.on_event('startup')
async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
