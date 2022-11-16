from os import getenv

import pika
from aio_pika import connect_robust
from pika.adapters.blocking_connection import BlockingChannel
from uvicorn.main import logger


class QueueConnection:
    GENERATE_PDF_QUEUE = 'generate-pdf'
    user = getenv("RABBITMQ_DEFAULT_USER")
    password = getenv("RABBITMQ_DEFAULT_PASS")
    hostname = getenv("RABBIT_HOSTNAME")
    connection: pika.BlockingConnection
    channel: BlockingChannel

    def __init__(self, process_callable):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(f"amqp://{self.user}:{self.password}@{self.hostname}:5672/%2F"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.GENERATE_PDF_QUEUE)
        self.process_callable = process_callable
        logger.info('Pika connection initialized')

    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        connection = await connect_robust(host=self.hostname,
                                          login=self.user,
                                          password=self.password,
                                          loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(self.GENERATE_PDF_QUEUE)
        await queue.consume(self.process_incoming_message, no_ack=False)
        logger.info('Established pika async listener')
        return connection

    async def process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        body: bytes = message.body
        logger.info('Received message')
        if body:
            if ex_handler(lambda: self.process_callable(body)):
                await message.ack()


def ex_handler(callable) -> bool:
    try:
        callable()
        return True
    except Exception as e:
        logger.error("Error while consuming message", exc_info=e)
        return False
