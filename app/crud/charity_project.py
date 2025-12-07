from typing import Optional

from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate
from app.core.constants import DAYS_IN_YEAR, DAYS_IN_MONTH


class CRUDCharityProject(CRUDBase[CharityProject, CharityProjectCreate]):
    async def get_project_by_name(
        self,
        session: AsyncSession,
        name: str,
    ) -> Optional[CharityProject]:
        result = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return result.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        duration = (
            (extract('year', CharityProject.close_date) -
             extract('year', CharityProject.create_date)) * DAYS_IN_YEAR +
            (extract('month', CharityProject.close_date) -
             extract('month', CharityProject.create_date)) * DAYS_IN_MONTH +
            (extract('day', CharityProject.close_date) -
             extract('day', CharityProject.create_date))
        )
        result = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested.is_(True),
            ).order_by(duration)
        )
        return result.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
