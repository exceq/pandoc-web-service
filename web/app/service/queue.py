import json
from os import getenv

import pika

from model.queue import GeneratePdfMessage


class QueueConnection:
    GENERATE_PDF_QUEUE = 'generate-pdf'
    user = getenv("RABBITMQ_DEFAULT_USER")
    password = getenv("RABBITMQ_DEFAULT_PASS")
    hostname = getenv("RABBIT_HOSTNAME")
    connection: pika.BlockingConnection

    def __init__(self):
        self.reopen_connection()
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.GENERATE_PDF_QUEUE)

    def reopen_connection(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(f"amqp://{self.user}:{self.password}@{self.hostname}:5672/%2F"))
        self.channel = self.connection.channel()

    def send_generate_pdf_message(self, msg: GeneratePdfMessage):
        if self.connection.is_closed:
            self.reopen_connection()
        if self.channel.is_closed:
            self.channel = self.connection.channel()

        self.channel.basic_publish('', self.GENERATE_PDF_QUEUE, body=bytes(json.dumps(msg.__dict__, ensure_ascii=False), 'utf-8'))
