# import json
# import threading

# import pika
# from django.db import transaction
# from .models import Event


# class Consumer(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         params = pika.URLParameters('amqps://nyyesqjn:9uRJdJxk6a6IXAygjawwdul5S0vwQXNa@cow.rmq2.cloudamqp.com/nyyesqjn')

#         connection = pika.BlockingConnection(params)
#         self.chanel = connection.channel()
#         self.chanel.queue_declare(queue='participant')

#     def callback(ch, method, properties, body):
#         print('Received in participant')
#         data = json.loads(body)
#         print(data)

#         with transaction.atomic():
#             if properties.content_type == 'event_created':
#                 event = Event.objects.create(id=data['id'], date=data['date'], name=data['name'])

#             elif properties.content_type == 'event_updated':
#                 event = Event.objects.get(id=data['id'])
#                 event.date = data['date']
#                 event.name = data['name']
#                 event.save()

#             elif properties.content_type == 'event_deleted':
#                 Event.objects.filter(id=data['id']).delete()

#         print('Transaction committed')

#     def run(self):
#         self.chanel.basic_consume(queue='participant', on_message_callback=self.callback, auto_ack=True)

#         print('started consuming')

#         self.chanel.start_consuming()
#         self.chanel.close()


from kombu import Connection, Exchange, Queue

def receive_message():
    with Connection('amqp://guest:guest@rabbitmq:5672//') as conn:
        exchange = Exchange("my_exchange", type="direct")
        queue = Queue("my_queue", exchange, routing_key="my_routing_key")
        consumer = conn.Consumer(queue, callbacks=[process_message])
        consumer.consume()

def process_message(body, message):
    print("Received message:", body)
    message.ack()
