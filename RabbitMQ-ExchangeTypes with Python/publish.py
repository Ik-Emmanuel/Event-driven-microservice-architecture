import pika
import json 
import uuid


""" Used for publishing messages """
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#declare your exchange 
channel.exchange_declare(
    exchange='order', #exchange name and type 
    exchange_type='direct'
)


#sample data to be published 
order = {
    "id": str(uuid.uuid4()), 
    "name": "Mr Test User",
    "product": "sweat shirts", 
    "quantity": 1
}


#publish  sample messages with different keys
"""Messages are sent to same exchange  but different routing keys for different queues"""
channel.basic_publish(
    exchange='order',
    routing_key='order.notify',
    body=json.dumps({'user_product': order['product'], 'user_name': order['name']})
)
print('💌 sent notify message')

channel.basic_publish(
    exchange='order',
    routing_key='order.report',
    body=json.dumps(order)
)
print('💌 sent report message')