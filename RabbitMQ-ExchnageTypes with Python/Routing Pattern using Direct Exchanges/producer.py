import pika
from pika.exchange_type import ExchangeType

#build connection
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

#define channel and declare exchange
channel = connection.channel()
channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)

#defined message to be published or use reusable functions that uses publish method
message = 'This message needs to be routed'
channel.basic_publish(exchange='routing', routing_key='analyticsonly', body=message)


print(f'sent message: {message}')
connection.close()