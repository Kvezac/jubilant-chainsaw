from fastapi import APIRouter, Depends, Cookie, Response
from src.app.delivery.schema import DeliveryCreateSchema, DeliverySchema, CategoriesSchema
from src.app.delivery.service import DeliveryService

router = APIRouter()


@router.post("/delivery", response_model=DeliverySchema)
async def create_delivery(
        body: DeliveryCreateSchema,
        session_id: str = Cookie(None),
        delivery_service: DeliveryService = Depends()
):
    session_id = await delivery_service.ensure_session(session_id)
    response = await delivery_service.create_delivery(body, session_id)
    response.set_cookie(key="session_id", value=session_id)
    return response


@router.get("/delivery/{delivery_id}", response_model=DeliverySchema)
async def get_delivery(
        delivery_id: int,
        session_id: str = Cookie(None),
        delivery_service: DeliveryService = Depends()
):
    session_id = await delivery_service.ensure_session(session_id)
    return await delivery_service.get_delivery(delivery_id, session_id)


@router.get("/categories", response_model=CategoriesSchema)
async def get_categories(delivery_service: DeliveryService = Depends()):
    return await delivery_service.get_categories()


@router.get("/categories/{category_id}", response_model=CategoriesSchema)
async def get_category_by_id(
        category_id: int,
        delivery_service: DeliveryService = Depends()
):
    return await delivery_service.get_category_id(category_id)
