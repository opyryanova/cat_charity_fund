from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount,
    check_project_exists,
    check_project_has_no_investments,
    check_project_is_open,
)
from app.core.constants import ErrorMessages
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectRead,
    CharityProjectUpdate,
)
from app.services.investment import invest_new_project

router = APIRouter()
get_session = Depends(get_async_session)


@router.post(
    '/',
    response_model=CharityProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = get_session,
):
    existing = await charity_project_crud.get_project_by_name(
        session, project_in.name
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.DUPLICATE_NAME.value,
        )
    new_project = await charity_project_crud.create(project_in, session)
    await invest_new_project(new_project, session)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectRead],
    response_model_exclude_none=True,
)
async def get_all_projects(session: AsyncSession = get_session):
    result = await session.execute(
        select(CharityProject).order_by(CharityProject.create_date)
    )
    return result.scalars().all()


@router.patch(
    '/{project_id}',
    response_model=CharityProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = get_session,
):
    project = await check_project_exists(project_id, session)
    check_project_is_open(project)
    if project_in.name:
        existing = await charity_project_crud.get_project_by_name(
            session, project_in.name
        )
        if existing and existing.id != project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.DUPLICATE_NAME.value,
            )
    if project_in.full_amount is not None:
        check_full_amount(project_in.full_amount, project)
        if project_in.full_amount == project.invested_amount:
            project.fully_invested = True
            project.close_date = datetime.utcnow()
    for field, value in project_in.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    await session.commit()
    await session.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = get_session,
):
    project = await check_project_exists(project_id, session)
    check_project_has_no_investments(project)
    await session.delete(project)
    await session.commit()
    return project
