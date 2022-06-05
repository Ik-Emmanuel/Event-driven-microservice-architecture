#import libraries
import pika
import time
import random


#define connection
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

#create channel and declare a queue
channel = connection.channel()
channel.queue_declare(queue='letterbox')


#continously piublish messages to be consumed by workers at random intervals between 1 and 3 secs
messageId = 1
while(True):
    message = f"Sending Message Id: {messageId}"
    channel.basic_publish(exchange='', routing_key='letterbox', body=message)
    print(f"sent message: {message}")
    time.sleep(random.randint(1, 4))
    messageId+=1