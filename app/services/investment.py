from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation


def close_if_fully_invested(obj: Union[CharityProject, Donation]) -> None:
    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.utcnow()


async def invest(
    source: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    if isinstance(source, CharityProject):
        targets = await donation_crud.not_fully_invested(session)
    else:
        targets = await charity_project_crud.not_fully_invested(session)

    for target in targets:
        if source.fully_invested:
            break

        amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount,
        )

        source.invested_amount += amount
        target.invested_amount += amount

        close_if_fully_invested(source)
        close_if_fully_invested(target)

        session.add(source)
        session.add(target)

    await session.commit()
    await session.refresh(source)
    return source


async def invest_new_project(
    project: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    return await invest(project, session)


async def invest_donation(
    donation: Donation,
    session: AsyncSession,
) -> Donation:
    return await invest(donation, session)
