import os

class Config():

    RMQ_LOGIN = os.environ.get("RMQ_LOGIN", "calc_mq")
    RMQ_PASSWORD = os.environ.get("RMQ_PASSWORD", "calcTemp111!")
    RMQ_HOST = os.environ.get("RMQ_HOST", "10.168.224.49")
    RMQ_PORT = os.environ.get("RMQ_PORT", "5672")
    RMQ_VIRTHOST = os.environ.get("RMQ_VIRTHOST", "calc_const")
