# #import pika, json

# # params = pika.URLParameters('amqps://nyyesqjn:9uRJdJxk6a6IXAygjawwdul5S0vwQXNa@cow.rmq2.cloudamqp.com/nyyesqjn')


# # connection = pika.BlockingConnection(params)
# # chanel = connection.channel()
# # def publish(method, body):
# #     #properties = pika.BasicProperties(method)
# #     #chanel.basic_publish(exchange='', routing_key='participant', body=json.dumps(body), properties=properties)


# from kombu import Connection, Exchange, Queue

# def send_message(message):
#     with Connection('amqp://guest:guest@rabbitmq:5672//') as conn:
#         exchange = Exchange("my_exchange", type="direct")
#         queue = Queue("my_queue", exchange, routing_key="my_routing_key")
#         producer = conn.Producer()
#         producer.publish(message, exchange=exchange, routing_key="my_routing_key")


