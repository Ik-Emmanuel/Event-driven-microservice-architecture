import pika, json

params = pika.URLParameters('amqps://svhpokuu:4Wg0rwXBfFpOlYL-jPpINpZ-j7erT5KH@woodpecker.rmq.cloudamqp.com/svhpokuu')
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)