import pika
from pika.exchange_type import ExchangeType

#define callback function to perform action upon receiving message
def on_message_received(ch, method, properties, body):
    """ Perform an action with the message body 
    or a series of actions by specifying different properties"""
    
    print(f'Analytics - received new message: {body}')

#build connection
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)


#define channel and declare topic exchange
channel = connection.channel()
channel.exchange_declare(exchange='topic', exchange_type=ExchangeType.topic)

#instantiate a queue to receive published messages and bind to an exchange thorough topics
queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='topic', queue=queue.method.queue, routing_key='*.europe.*')

#consume received  messages
channel.basic_consume(queue=queue.method.queue, auto_ack=True,
    on_message_callback=on_message_received)

print('Analytics Starting Consuming')
channel.start_consuming()