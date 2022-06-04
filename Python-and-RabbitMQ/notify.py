import pika
import json 

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('order_notify')
queue_name = queue.method.queue

#create binding
channel.queue_bind(
    exchange="order",
    queue=queue_name,
    routing_key='order.notify'  #this is the binding key

)

#the consumer
def callback(ch, method, properties, body):
    payload = json.loads(body)
    print (f"🔰 Notifying: { payload['user_name']} on {payload['user_product']}")
    print('✅Done')
    # send acknowledgement to rabbitmQ to confirm that 
    # message was received and consumed and it is free to delete until this is done, the message is kept for the consumer incase it was unavailable.
    ch.basic_ack(delivery_tag=method.delivery_tag)

#message consumption
channel.basic_consume(on_message_callback=callback, queue=queue_name )
print('💤 Waiting for notify messages. To exit, press CTRL+ C')

channel.start_consuming()