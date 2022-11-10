import json
from os import getenv

import pika

from model.queue import GeneratePdfMessage


class QueueConnection:
    GENERATE_PDF_QUEUE = 'generate-pdf'

    def __init__(self):
        user = getenv("RABBITMQ_DEFAULT_USER")
        password = getenv("RABBITMQ_DEFAULT_PASS")
        hostname = getenv("RABBIT_HOSTNAME")
        self.connection = pika.BlockingConnection(pika.URLParameters(f"amqp://{user}:{password}@{hostname}:5672/%2F"))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.GENERATE_PDF_QUEUE)
        self.connection.channel()

    def send_generate_pdf_message(self, msg: GeneratePdfMessage):
        if self.channel.is_closed:
            self.channel = self.connection.channel()
        self.channel.basic_publish('', self.GENERATE_PDF_QUEUE, body=bytes(json.dumps(msg.__dict__), 'utf-8'))
