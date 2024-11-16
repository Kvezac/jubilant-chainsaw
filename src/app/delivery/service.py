from dataclasses import dataclass
from src.app.delivery.repository.delevery import DeliveryRepository
from src.app.delivery.repository.cache_tools import RedisTools
from src.app.delivery.schema import DeliverySchema, DeliveryCreateSchema, CategoriesSchema
from src.app.delivery.repository.calculate import Calculate
from fastapi import HTTPException, Cookie

from src.app.exception import DeliveryNotFound


@dataclass
class DeliveryService:
    delivery_repository: DeliveryRepository
    cache_tools: RedisTools
    calculate: Calculate

    async def create_delivery(self, body: DeliveryCreateSchema, session_id: str) -> DeliverySchema:
        delivery = await self.delivery_repository.create(body, session_id)
        return delivery

    async def get_delivery(self, delivery_id: int, session_id: str) -> DeliverySchema:
        delivery = await self.delivery_repository.get(delivery_id, session_id)
        if not delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")
        return delivery

    async def get_categories(self) -> CategoriesSchema:
        categories = await self.delivery_repository.get_categories()
        return categories

    async def get_category_id(self, category_id: int) -> CategoriesSchema:
        category = await self.delivery_repository.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    async def update_shipping_cost(self, delivery_id: int) -> DeliverySchema:
        delivery = await self.delivery_repository.get_delivery(delivery_id=delivery_id)
        if not delivery:
            raise DeliveryNotFound
        dolar_rate = await self.cache_tools.get_pair('USD')
        shipping_cost = self.calculate.calculate_cost(delivery.weight, delivery.content_value, dolar_rate)
        updated_delivery = await self.delivery_repository.update_cost(delivery_id=delivery_id,
                                                                      shipping_cost=shipping_cost)
        return updated_delivery

    async def ensure_session(self, session_id: str) -> str:
        if not session_id:
            session_id = self.calculate.create_session_token()
            await self.cache_tools.set_session(session_id)
        return session_id
