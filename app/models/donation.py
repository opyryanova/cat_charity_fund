from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class Donation(Base):
    __tablename__ = 'donation'

    id = Column(Integer, primary_key=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    close_date = Column(DateTime, nullable=True)
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='donations')
