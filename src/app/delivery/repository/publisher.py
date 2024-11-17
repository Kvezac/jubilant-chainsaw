import aio_pika
from src.app.infrastructure.broker.rabbit_connection import get_rabbitmq_connection, get_rabbitmq_channel, declare_queue


async def send_id_to_queue(session_id: int):
    connection = await get_rabbitmq_connection()
    channel = await get_rabbitmq_channel()
    queue = await declare_queue(channel, "model_queue")

    message = aio_pika.Message(body=str(session_id).encode())
    await channel.default_exchange.publish(message, routing_key=queue.name)

    await connection.close()
