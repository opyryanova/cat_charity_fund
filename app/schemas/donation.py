from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    class Config:
        extra = Extra.forbid


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
        extra = Extra.forbid


class DonationFullInfoDB(DonationDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
        extra = Extra.forbid
