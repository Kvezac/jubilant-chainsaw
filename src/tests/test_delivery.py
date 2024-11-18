import logging

import pytest
from httpx import AsyncClient

from src.app.logger.common import configure_logging
from src.app.main import create_app

# Настройка логирования
configure_logging()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
async def test_app(db_engine):
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_ping_db(delivery_repository):
    logger.info("Testing database ping...")
    response = await delivery_repository.ping_db()
    assert response == {"text": "db is working"}
    logger.info("Database ping successful.")


@pytest.mark.asyncio
async def test_create_category(test_app, db_session):
    logger.info("Creating a new category...")
    response = await test_app.post("/categories/", json={"name": "Test Category"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Category"
    logger.info("Category created: %s", response.json())


@pytest.mark.asyncio
async def test_create_delivery(test_app, db_session):
    logger.info("Creating a new category for delivery...")
    category_response = await test_app.post("/categories/", json={"name": "Test"})
    category_id = category_response.json()["id"]

    delivery_data = {
        "name": "Test Delivery",
        "weight": 10.5,
        "type_id": category_id,
        "user_session": "test_session",
        "content_value": 100.0
    }

    logger.info("Creating a new delivery...")
    response = await test_app.post("/deliveries/", json=delivery_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Delivery"
    logger.info("Delivery created: %s", response.json())
