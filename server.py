import logging
import json
from typing import Any
from time import sleep
import aio_pika
from aio_pika.channel import Channel
from aio_pika import connect, Message
from config import Config

BROKER_CONNECTION = None
BROKER_CHANNEL = None

class Error(Exception):
    def __init__(self,*args):
        if args:
            self.message = args[0]
        else:
            self.message = None
        logging.basicConfig(filename='error.log',filemode="w", encoding='utf-8', level=logging.DEBUG)


class MessageQueue():


    async def send_rabbitmq(self, queue_name: str, data: Any):
        connection = await connect(f"amqp://{Config.RMQ_LOGIN}:{Config.RMQ_PASSWORD}@{Config.RMQ_HOST}:{Config.RMQ_PORT}/{Config.RMQ_VIRTHOST}")
        channel = await connection.channel()
        message=Message(json.dumps(data).encode("utf-8"))
        await channel.default_exchange.publish(message,queue_name)
        await connection.close()


    async def add_queue_rabbitmq(self, queue_name: str):
        connection = await connect(f"amqp://{Config.RMQ_LOGIN}:{Config.RMQ_PASSWORD}@{Config.RMQ_HOST}:{Config.RMQ_PORT}/{Config.RMQ_VIRTHOST}")
        channel = await connection.channel()
        await channel.declare_queue(queue_name,durable=True)
        await connection.close()


    async def delete_queue_rabbitmq(self, queue_name: str):
        connection = await connect (f"amqp://{Config.RMQ_LOGIN}:{Config.RMQ_PASSWORD}@{Config.RMQ_HOST}:{Config.RMQ_PORT}/{Config.RMQ_VIRTHOST}")
        channel = await connection.channel()
        await channel.queue_delete(queue_name)
        await connection.close()


async def connect_to_broker() -> Channel:

    global BROKER_CONNECTION
    global BROKER_CHANNEL

    retries = 0
    while not BROKER_CONNECTION:
        conn_str = f"amqp://{Config.RMQ_LOGIN}:{Config.RMQ_PASSWORD}@{Config.RMQ_HOST}:{Config.RMQ_PORT}/{Config.RMQ_VIRTHOST}"
        print(f"Trying to create connection to broker: {conn_str}")
        try:
            BROKER_CONNECTION = await aio_pika.connect_robust(conn_str)
            print(f"Connected to broker ({type(BROKER_CONNECTION)} ID {id(BROKER_CONNECTION)})")
        except Exception as e:
            retries += 1
            print(f"Can't connect to broker {retries} time({e.__class__.__name__}:{e}). Will retry in 5 seconds...")
            sleep(5)

    if not BROKER_CHANNEL:
        print("Trying to create channel to broker")
        BROKER_CHANNEL = await BROKER_CONNECTION.channel()
        print("Got a channel to broker")

    return BROKER_CHANNEL

mq = MessageQueue()


