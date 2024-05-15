# tasks.py

from celery import Celery

app = Celery('tasks', backend='amqp://localhost', broker='amqp://guest:guest@localhost//')

@app.task(name="add", queue="data_queue", exchange="celery")
def add(x, y):
    return x + y
