import pika
from pika.exchange_type import ExchangeType

#build a connection
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

#define a channel and declare and exchange
channel = connection.channel()
channel.exchange_declare(exchange='topic', exchange_type=ExchangeType.topic)

#publish multiple messages through Topics 

#define your message body or use a function to get data to be published 
user_payments_message = 'A european user paid for something'
channel.basic_publish(exchange='topic', routing_key='user.europe.payments', body=user_payments_message)
print(f'sent message: {user_payments_message}')

#define your message body or use a function to get data to be published 
business_order_message = 'A european business ordered goods'
channel.basic_publish(exchange='topic', routing_key='business.europe.order', body=business_order_message)
print(f'sent message: {business_order_message}')


connection.close()