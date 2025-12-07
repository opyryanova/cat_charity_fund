from fastapi import APIRouter

from app.api.endpoints import charity_project, donation, user, google_api

api_router = APIRouter()
api_router.include_router(
    charity_project.router,
    prefix='/charity_project',
    tags=['charity_projects'],
)
api_router.include_router(
    donation.router,
    prefix='/donation',
    tags=['donations'],
)
api_router.include_router(user.router)
api_router.include_router(
    google_api.router,
    prefix='/google',
    tags=['Google'],
)
