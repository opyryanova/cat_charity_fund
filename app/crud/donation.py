from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation, DonationCreate]):
    async def get_multi(self, session: AsyncSession):
        result = await session.execute(select(Donation))
        return result.scalars().all()

    async def get_by_user(self, user_id: int, session: AsyncSession):
        result = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return result.scalars().all()


donation_crud = CRUDDonation(Donation)
