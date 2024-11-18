import logging

import pytest
from sqlalchemy import select

from src.app.delivery.models import Categories
from src.app.logger.common import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_ping_db(delivery_repository):
    logger.info("Testing database ping...")
    response = await delivery_repository.ping_db()
    assert response == {"text": "db is working"}
    logger.info("Database ping successful.")


@pytest.mark.asyncio
async def test_insert_initial_data(db_session):
    categories_types = ["одежда", "электроника", "разное"]

    query = select(Categories)
    result = await db_session.scalars(query)

    if not result.all():
        for pt in categories_types:
            db_session.add(Categories(name=pt))
        await db_session.commit()

    query = select(Categories)
    result = await db_session.scalars(query)
    categories_types = result.all()

    assert len(categories_types) == 3
    assert {pt.name for pt in categories_types} == {
        "одежда",
        "электроника",
        "разное",
    }


@pytest.mark.asyncio
async def test_create_delivery(test_app, db_session):
    logger.info("Creating  for delivery...")
    category_response = await test_app.post("/categories/", json={"name": "одежда"})
    category_id = category_response.json()["id"]

    delivery_data = {
        "name": "Delivery",
        "weight": 10.5,
        "type_id": category_id,
        "user_session": "одежда",
        "content_value": 100.0
    }

    logger.info("Creating a new delivery...")
    response = await test_app.post("/deliveries/", json=delivery_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Delivery"
    logger.info("Delivery created: %s", response.json())


@pytest.mark.asyncio
async def test_negative_delivery(test_app, db_session):
    logger.info("Creating for negative delivery...")
    category_response = await test_app.post("/categories/", json={"name": "одежда"})
    category_id = category_response.json()["id"]

    delivery_data = {
        "name": "Delivery",
        "weight": 'aaa',
        "type_id": category_id,
        "user_session": "одежда",
        "content_value": 100.0
    }

    logger.info("Creating a negative delivery...")
    response = await test_app.post("/deliveries/", json=delivery_data)
    assert response.status_code == 422
    assert response.json()["name"] == "Delivery"
    logger.info("Delivery not created: %s", response.json())
