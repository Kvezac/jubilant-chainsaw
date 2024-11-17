from src.app.dependecies import get_delivery_repository
from src.app.infrastructure.tasks.accessor import celery


def get_delivery_service():
    return get_delivery_repository()


@celery.task
def update_chipping_coast_task(session_id):
    delivery_service = get_delivery_service()
    delivery_service.update_shipping_cost(session_id)
