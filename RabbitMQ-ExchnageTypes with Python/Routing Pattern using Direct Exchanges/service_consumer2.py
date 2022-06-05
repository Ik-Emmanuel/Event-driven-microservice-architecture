import pika
from pika.exchange_type import ExchangeType


#defined callback function to handle received event message
def on_message_received(ch, method, properties, body):
    """ Perform an action with the message body 
    or a series of actions by specifying different properties"""
    
    print(f'Service2 - received new message: {body}')

#build connection
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

#define channel and declare exchange
channel = connection.channel()
channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)

#instantiate your queue
queue = channel.queue_declare(queue='', exclusive=True)

#allow for multiple message receiving by binding using multiple routing_keys
channel.queue_bind(exchange='routing', queue=queue.method.queue, routing_key='paymentsonly')
channel.queue_bind(exchange='routing', queue=queue.method.queue, routing_key='both')

#define consumption logic
channel.basic_consume(queue=queue.method.queue, auto_ack=True,
    on_message_callback=on_message_received)

print('Service 2 Starting Consuming')
channel.start_consuming()