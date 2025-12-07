from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.donation import Donation
from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    __allow_unmapped_annotations__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    donations: Mapped[List['Donation']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
