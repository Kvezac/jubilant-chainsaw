from src.app.delivery.rabbit import consume_messages
from src.app.delivery.service import DeliveryService


async def process_task(session_id: str):
    await DeliveryService.update_shipping_cost(session_id)


async def start_consuming():
    await consume_messages(process_task)
