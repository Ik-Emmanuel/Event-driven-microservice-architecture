import pika

#define callback function to consume requests and send replies 
def on_request_message_received(ch, method, properties, body):
    """ Perform an action with the request body or a series of actions by specifying different properties"""
    print(f"Received Request: {properties.correlation_id}, {body}")
    ch.basic_publish('', routing_key=properties.reply_to, body=f'Hey its your reply to {properties.correlation_id}')

#build connections
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

#define channels and declare the queue
channel = connection.channel()
channel.queue_declare(queue='request-queue')

#consume incoming messages from the exchange
channel.basic_consume(queue='request-queue', auto_ack=True,
    on_message_callback=on_request_message_received)

print("Starting Server")
channel.start_consuming()