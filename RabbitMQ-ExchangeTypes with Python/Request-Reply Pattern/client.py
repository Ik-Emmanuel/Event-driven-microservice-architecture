import pika
import uuid

#define function to consume reply from server 
def on_reply_message_received(ch, method, properties, body):
    """ Perform an action with the response body or a series of actions by specifying different properties"""
    print(f"reply received: {body}")


#build a connection with url
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

#define channel and instantiate a queue to receive response or reply
channel = connection.channel()
reply_queue = channel.queue_declare(queue='', exclusive=True)

#start listening for replies on the defined queue
channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True,
    on_message_callback=on_reply_message_received)

#define another queue to receive requests
channel.queue_declare(queue='request-queue')

#defined a correlation_id to specify to the server which client sent the requests
cor_id = str(uuid.uuid4())
print(f"Sending Request: {cor_id}")

#publish messages to the server with corr_id and specify the reply queue server should use 
channel.basic_publish('', routing_key='request-queue', properties=pika.BasicProperties(
    reply_to=reply_queue.method.queue,
    correlation_id=cor_id
), body='Can I request a reply?')

#start client and listen for replies 
print("Starting Client")
channel.start_consuming()