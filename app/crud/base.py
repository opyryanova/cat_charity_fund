from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        user: Optional[object] = None,
    ) -> ModelType:
        obj_data = obj_in.dict()
        if user is not None and hasattr(self.model, 'user_id'):
            obj_data['user_id'] = user.id

        db_obj = self.model(**obj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get(
        self,
        session: AsyncSession,
        obj_id: int,
    ) -> Optional[ModelType]:
        return await session.get(self.model, obj_id)

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: BaseModel,
    ) -> ModelType:
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        session: AsyncSession,
        db_obj: ModelType,
    ) -> None:
        await session.delete(db_obj)
        await session.commit()

    async def not_fully_invested(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        result = await session.execute(
            select(self.model).where(self.model.fully_invested.is_(False))
        )
        return result.scalars().all()
