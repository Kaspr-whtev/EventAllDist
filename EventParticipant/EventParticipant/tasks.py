# from EventParticipant.celery_config import app


# @app.task(name="EventParticipant.participant_task", queue="data_queue", exchange="celery")
# def participant_task(arg1, arg2):
#     raise NotImplementedError()

# tasks.py

# from celery import Celery
#
# app = Celery('tasks', backend='amqp://localhost', broker='amqp://guest:guest@localhost//')
#
# @app.task(name="add", queue="data_queue", exchange="celery")
# def add(x, y):
#     print(x)
