from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import ErrorMessages
from app.models.charity_project import CharityProject


async def check_project_name_unique(
    project_name: str,
    session: AsyncSession,
) -> None:
    result = await session.execute(
        select(CharityProject).where(CharityProject.name == project_name)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.DUPLICATE_NAME.value,
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await session.get(CharityProject, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.PROJECT_NOT_FOUND.value,
        )
    return project


def check_project_is_open(project: CharityProject) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.PROJECT_CLOSED.value,
        )


def check_full_amount_not_less_than_invested(
    new_amount: int,
    project: CharityProject,
) -> None:
    if new_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.FULL_AMOUNT_LESS_THAN_INVESTED.value,
        )


def check_project_has_no_investments(project: CharityProject) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.PROJECT_HAS_INVESTMENTS.value,
        )
