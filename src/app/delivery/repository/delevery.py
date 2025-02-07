from decimal import Decimal

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from src.app.delivery.models import Deliveries, Categories
from src.app.delivery.schema import DeliveryCreateSchema


class DeliveryRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def ping_db(self) -> None:
        async with self.db_session as session:
            try:
                await session.execute(text("SELECT 1"))
            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database is not available")
            return {"text": "db is working"}

    async def get_delivery(self, delivery_id: int) -> Deliveries | None:
        async with self.db_session as session:
            delivery: Deliveries = (
                await session.execute(select(Deliveries).where(Deliveries.id == delivery_id))).scalar_one_or_none()
        return delivery

    async def get_user_delivery(self, delivery_id: int, session_id: int) -> Deliveries | None:
        query = (
            select(Deliveries)
            .join(Categories, Categories.id == Deliveries.category_id)
            .where(Deliveries.id == delivery_id, Deliveries.session_id == session_id)
        )
        async with self.db_session as session:
            try:
                delivery: Deliveries = (await session.execute(query)).scalar_one_or_none()
                return delivery
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def create_delivery(self, delivery: DeliveryCreateSchema) -> int:
        query = (
            insert(Deliveries)
            .values(name=delivery.name, weight=delivery.weight, type_id=delivery.type_id,
                    user_session=delivery.user_session, content_cost=delivery.content_cost)
            .returning(Deliveries.id)
        )
        async with self.db_session as session:
            delivery_id = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return delivery_id

    async def get_all_category(self) -> list[Categories]:
        query = (
            select(Categories)
        )
        async with self.db_session as session:
            categories: list[Categories] = (await session.execute(query)).scalars().all()
            return categories

    async def update_delivery_price(self, delivery_id: int, cost_shipping: Decimal) -> Deliveries:
        query = update(Deliveries).where(Deliveries.id == delivery_id).values(cost_chipping=cost_shipping).returning(
            Deliveries.id)
        async with self.db_session as session:
            task_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return await self.get_task(task_id)

    async def get_category_id(self, category_id: int) -> Categories | None:
        query = select(Categories.id).where(Categories.id == category_id)

        async with self.db_session as session:
            result = (await session.execute(query)).scalar_one_or_none()
            return result

    async def _create_category_data(self):
        async with self.db_session as session:
            category_type = ["одежда", "электроника", "разное"]
            query = select(Categories)
            result = await session.scalars(query)
            if not result.all():
                for category in category_type:
                    session.add(Categories(name=category))
                await session.commit()
