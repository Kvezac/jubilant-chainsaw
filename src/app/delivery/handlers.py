import logging
from fastapi import APIRouter, Depends, Cookie, Response
from src.app.dependecies import get_delivery_repository
from src.app.delivery.schema import DeliveryCreateSchema, DeliverySchema, CategoriesSchema
from src.app.delivery.service import DeliveryService
from src.app.logger.common import configure_logging
from src.app.delivery.tasks import update_chipping_coast_task

configure_logging()
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/delivery', tags=["delivery"])


@router.post("/", response_model=DeliverySchema)
async def create_delivery(
        delivery: DeliveryCreateSchema,
        session_id: str = Cookie(None),
        delivery_service: DeliveryService = Depends(get_delivery_repository)
):
    logger.info(f"Creating delivery with data: {delivery}")
    session_id = await delivery_service.ensure_session(session_id)
    response = await delivery_service.create_delivery(delivery, session_id)
    response_obj = Response(content=response.json())
    response_obj.set_cookie(key="session_id", value=session_id)
    update_chipping_coast_task.dealay(session_id)
    return response_obj


@router.get("/{delivery_id}", response_model=DeliverySchema)
async def get_delivery(
        delivery_id: int,
        session_id: str = Cookie(None),
        delivery_service: DeliveryService = Depends(get_delivery_repository)
):
    logger.info(f"Fetching delivery with ID: {delivery_id}")
    session_id = await delivery_service.ensure_session(session_id)
    logger.debug(f"Ensured session ID: {session_id}")
    delivery = await delivery_service.get_delivery(delivery_id, session_id)
    logger.info(f"Fetched delivery: {delivery}")
    return delivery


@router.get("/categories", response_model=list[CategoriesSchema])
async def get_categories(delivery_service: DeliveryService = Depends(get_delivery_repository)):
    logger.info("Fetching all categories")
    categories = await delivery_service.get_categories()
    logger.info(f"Fetched categories: {categories}")
    return categories


@router.get("/categories/{category_id}", response_model=CategoriesSchema)
async def get_category_by_id(
        category_id: int,
        delivery_service: DeliveryService = Depends(get_delivery_repository)
):
    logger.info(f"Fetching category with ID: {category_id}")
    category = await delivery_service.get_category_id(category_id)
    logger.info(f"Fetched category: {category}")
    return category
