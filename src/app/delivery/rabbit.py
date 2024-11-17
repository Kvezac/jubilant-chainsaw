import aio_pika
from src.app.config import settings

RABBITMQ_URL = settings.get_rabbitmq_url
queue_name = "task_queue"


async def get_rabbit_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)


async def publish_message(message: str):
    async with get_rabbit_connection() as connection:
        async with connection.channel() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=queue_name,
            )


async def consume_messages(callback):
    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        async for message in queue:
            async with message.process():
                await callback(message.body.decode())
