#import libraries 
import pika
import time
import random


#define callback function
def on_message_received(ch, method, properties, body):
    """ Perform an action with the message body 
    or a series of actions by specifying different properties"""
    
    processing_time = random.randint(1, 6)
    print(f'received: "{body}", will take {processing_time} to process')
    time.sleep(processing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f'finished processing and acknowledged message')

#create connection
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

#instantiate channel 
channel = connection.channel()
channel.queue_declare(queue='letterbox')

#This tells the exchange not to send another message until its done processing the current one
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='letterbox', on_message_callback=on_message_received)
print('Starting Consuming')

channel.start_consuming()