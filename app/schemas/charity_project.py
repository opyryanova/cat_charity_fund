from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt, constr

from app.core.constants import (
    PROJECT_DESC_MIN_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_NAME_MIN_LENGTH,
)


class CharityProjectBase(BaseModel):
    name: constr(
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH,
    )
    description: constr(min_length=PROJECT_DESC_MIN_LENGTH)
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(BaseModel):
    name: Optional[
        constr(
            min_length=PROJECT_NAME_MIN_LENGTH,
            max_length=PROJECT_NAME_MAX_LENGTH,
        )
    ] = None
    description: Optional[constr(min_length=PROJECT_DESC_MIN_LENGTH)] = None
    full_amount: Optional[PositiveInt] = None

    class Config:
        extra = Extra.forbid


class CharityProjectRead(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
        extra = Extra.forbid
