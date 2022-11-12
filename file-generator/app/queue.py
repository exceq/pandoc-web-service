from os import getenv

import pika
from pika.adapters.blocking_connection import BlockingChannel


class QueueConnection:
    GENERATE_PDF_QUEUE = 'generate-pdf'
    user = getenv("RABBITMQ_DEFAULT_USER")
    password = getenv("RABBITMQ_DEFAULT_PASS")
    hostname = getenv("RABBIT_HOSTNAME")
    connection: pika.BlockingConnection
    channel: BlockingChannel

    def __init__(self):
        self.reopen_connection()
        self.channel.queue_declare(queue=self.GENERATE_PDF_QUEUE)

    def reopen_connection(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(f"amqp://{self.user}:{self.password}@{self.hostname}:5672/%2F"))
        self.channel = self.connection.channel()
