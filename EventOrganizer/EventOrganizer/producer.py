import pika, json

params = pika.URLParameters('amqps://nyyesqjn:9uRJdJxk6a6IXAygjawwdul5S0vwQXNa@cow.rmq2.cloudamqp.com/nyyesqjn')


connection = pika.BlockingConnection(params)
chanel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    chanel.basic_publish(exchange='', routing_key='participant', body=json.dumps(body), properties=properties)
