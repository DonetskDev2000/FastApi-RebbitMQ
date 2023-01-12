from fastapi import FastAPI,Query
from server import mq, connect_to_broker, Error

app = FastAPI(title="Working with RebbitMQ queues")

successful_message=0

@app.on_event('startup')
async def start_message_consuming():
    channel = await connect_to_broker()
    mq.channel = channel


@app.post("/add_message",name="Добавление сообщения в очередь", operation_id="add_message")
async def add_message(queue:str = Query(None),task:str = Query(None)):
    try:
        global successful_message
        await mq.send_rabbitmq(queue,task)
        successful_message += 1
        return {"message": f"{task}"}
    except Exception as error:
        raise Error(error)


@app.post("/add_queue",name="Добавление очереди", operation_id="add_queue")
async def add_message(queue:str = Query(None)):
    try:
        await mq.add_queue_rabbitmq(queue)
    except Exception as error:
        raise Error(error)


@app.post("/delete_queue",name="Удаление очереди", operation_id="delete_queue")
async def add_message(queue:str = Query(None)):
    try:
        await mq.delete_queue_rabbitmq(queue)
    except Exception as error:
        raise Error(error)


@app.get("/stats")
def get_stats():
    global successful_message
    return successful_message





