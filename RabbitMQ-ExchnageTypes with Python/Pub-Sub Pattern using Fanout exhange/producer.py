import pika
from pika.exchange_type import ExchangeType

#build connection
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

#define channel and declare  fan out exchange
channel = connection.channel()
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)


#build your message or defined custom helper function that takes message to be published 
message = "Hello I want to broadcast this message"
channel.basic_publish(exchange='pubsub', routing_key='', body=message)

#confirm message is sent 
print(f"sent message: {message}")

connection.close()