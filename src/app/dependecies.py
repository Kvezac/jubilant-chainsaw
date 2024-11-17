from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.delivery.repository.delevery import DeliveryRepository
from src.app.infrastructure.database.accessor import get_db_session


async def get_delivery_repository(db_session: AsyncSession = Depends(get_db_session)) -> DeliveryRepository:
    return DeliveryRepository(db_session)
