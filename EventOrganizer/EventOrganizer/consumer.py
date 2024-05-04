import json
import threading

import pika


class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        params = pika.URLParameters('amqps://nyyesqjn:9uRJdJxk6a6IXAygjawwdul5S0vwQXNa@cow.rmq2.cloudamqp.com/nyyesqjn')

        connection = pika.BlockingConnection(params)
        self.chanel = connection.channel()
        self.chanel.queue_declare(queue='organizer')

    def callback(ch, method, properties, body):
        print('Received in organizer')
        message = json.loads(body)
        print(message)

    def run(self):
        self.chanel.basic_consume(queue='organizer', on_message_callback=self.callback, auto_ack=True)

        print('started consuming')

        self.chanel.start_consuming()
        self.chanel.close()
