import pika

#defined callback function 
def on_message_received(ch, method, properties, body):
    """ Perform an action with the message body 
    or a series of actions by specifying different properties"""

    print(f"first_consumer - received new message: {body}")

#build connection
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

#set up channel and bind to an exchange
channel = connection.channel()
channel.exchange_declare(exchange='pubsub', exchange_type='fanout')

#declare a queue and bind queue to exchange Server generates a name accessed with : queue.method.queue
queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='pubsub', queue=queue.method.queue)

#defined message queue consumption with callback function
channel.basic_consume(queue=queue.method.queue, auto_ack=True,
    on_message_callback=on_message_received)

#start consuming
print("Starting Consuming")
channel.start_consuming()