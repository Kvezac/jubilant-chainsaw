from src.app.delivery.repository.delevery import DeliveryRepository
from src.app.delivery.service import DeliveryService
from src.app.infrastructure.database.accessor import get_db_session
from src.app.infrastructure.tasks.accessor import celery


@celery.task
async def update_chipping_cost_task(session_id: str):
    async with get_db_session() as db_session:
        delivery_service = DeliveryService(
            delivery_repository=DeliveryRepository(db_session),
        )
        await delivery_service.update_shipping_cost(session_id)
