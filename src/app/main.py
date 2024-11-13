import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi_utils.tasks import repeat_every

from src.app.delivery.repository.events import get_currency_exchange_rate as exchange
from src.app.delivery.handlers import router as delivery_router


def create_app() -> FastAPI:
    app = FastAPI(
        debug=True,
        docs_url='/auth/docs',
        title="Test save secret cookie to redis",
    )

    app.include_router(delivery_router)
    app.include_router(health_router)

    @app.on_event('startup')
    @repeat_every(seconds=60 * 60 * 24)  # каждые 24 часа
    async def start_exchange():
        await exchange()

    return app


health_router = APIRouter(prefix='/health', tags=['health app'])


@health_router.get('/',
                   description='health app',
                   )
def health_check() -> dict[str, str]:
    return {'status': 'app is healthy'}


if __name__ == '__main__':
    uvicorn.run(app='main:create_app', reload=True, host='localhost', port=8000)
