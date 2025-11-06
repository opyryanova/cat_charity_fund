from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.constants import PROJECT_NAME_MAX_LENGTH
from app.core.db import Base


class CharityProject(Base):
    __tablename__ = 'charityproject'

    id = Column(Integer, primary_key=True)
    name = Column(
        String(PROJECT_NAME_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    close_date = Column(DateTime, nullable=True)
