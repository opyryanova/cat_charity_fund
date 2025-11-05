from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import Donation
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.investment import invest_donation

router = APIRouter()
get_session = Depends(get_async_session)
get_user = Depends(current_user)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = get_session,
    user=get_user,
):
    donation = await donation_crud.create(donation_in, session, user)
    await invest_donation(donation, session)
    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
)
async def get_all_donations(session: AsyncSession = get_session):
    result = await session.execute(
        select(Donation).order_by(Donation.create_date)
    )
    return result.scalars().all()
