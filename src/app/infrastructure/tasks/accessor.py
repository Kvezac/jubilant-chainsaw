from celery import Celery

from src.app.config import settings

celery = Celery("tasks", broker=settings.get_rabbitmq_url,
                include="src.app.delivery.tasks")
