import logging
from dataclasses import dataclass

from fastapi import HTTPException

from src.app.delivery.repository.cache_tools import RedisTools
from src.app.delivery.repository.calculate import Calculate
from src.app.delivery.repository.delevery import DeliveryRepository
from src.app.delivery.schema import DeliverySchema, DeliveryCreateSchema, CategoriesSchema
from src.app.exception import DeliveryNotFound, DollarNotFound
from src.app.logger.common import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


@dataclass
class DeliveryService:
    delivery_repository: DeliveryRepository
    cache_tools: RedisTools
    calculate: Calculate

    async def create_delivery(self, body: DeliveryCreateSchema, session_id: str) -> DeliverySchema:
        delivery = await self.delivery_repository.create(body, session_id)
        logger.info(f"Delivery created with ID: {delivery.id}")
        return delivery

    async def get_delivery(self, delivery_id: int, session_id: str) -> DeliverySchema:
        delivery = await self.delivery_repository.get(delivery_id, session_id)
        if not delivery:
            logger.warning(f"Delivery with ID {delivery_id} not found")
            raise HTTPException(status_code=404, detail="Delivery not found")
        logger.info(f"Fetched delivery: {delivery}")
        return delivery

    async def get_categories(self) -> list[CategoriesSchema]:
        logger.info("Fetching all categories")
        categories = await self.delivery_repository.get_categories()
        logger.info(f"Fetched categories: {categories}")
        return categories

    async def get_category_id(self, category_id: int) -> CategoriesSchema:
        logger.info(f"Fetching category with ID: {category_id}")
        category = await self.delivery_repository.get_category(category_id)
        if not category:
            logger.warning(f"Category with ID {category_id} not found")
            raise HTTPException(status_code=404, detail="Category not found")
        logger.info(f"Fetched category: {category}")
        return category

    async def update_shipping_cost(self, delivery_id: int) -> DeliverySchema:
        delivery = await self.delivery_repository.get_delivery(delivery_id=delivery_id)
        if not delivery:
            logger.error(f"Delivery with ID {delivery_id} not found")
            raise DeliveryNotFound
        dollar_rate = await self.cache_tools.get_pair('rate_usd')
        if not dollar_rate:
            logger.error("Dollar rate not found")
            raise DollarNotFound
        shipping_cost = self.calculate.calculate_cost(delivery.weight, delivery.content_value, dollar_rate)
        updated_delivery = await self.delivery_repository.update_cost(delivery_id=delivery_id,
                                                                      shipping_cost=shipping_cost)
        logger.info(f"Updated delivery: {updated_delivery}")
        return updated_delivery

    async def ensure_session(self, session_id: str) -> str:
        if not session_id:
            session_id = self.calculate.create_session_token()
            await self.cache_tools.set_session(session_id)
        else:
            logger.info(f"Using existing session with ID: {session_id}")
        return session_id
