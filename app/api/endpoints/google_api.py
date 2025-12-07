from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectRead
from app.services.google_api import (
    create_spreadsheets,
    set_user_permissions,
    update_spreadsheets_value,
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectRead],
    dependencies=[Depends(current_superuser)],
    tags=['Google'],
)
async def get_google_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
) -> list[CharityProjectRead]:
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session,
    )
    spreadsheet_id = await create_spreadsheets(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await update_spreadsheets_value(
        spreadsheet_id,
        projects,
        wrapper_services,
    )
    return projects
