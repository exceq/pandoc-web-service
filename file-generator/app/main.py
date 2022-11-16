import asyncio

from fastapi import FastAPI

from service.generator import handle_message
from service.queue import QueueConnection

app = FastAPI()

pika_client = QueueConnection(handle_message)


@app.get("/")
async def root():
    return {"message": "Hello World from file-generator"}


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(pika_client.consume(loop))
    await task
