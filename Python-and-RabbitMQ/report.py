import pika
import json 

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('order_report')
queue_name = queue.method.queue

#create binding
channel.queue_bind(
    exchange="order",
    queue=queue_name,
    routing_key='order.report'  #this is the binding key

)

#the consumer
def callback(ch, method, properties, body):
    payload = json.loads(body)
    print (f"🔰 Generating Report")
    print(payload)
    print('✅Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)

#message consumption
channel.basic_consume(on_message_callback=callback, queue=queue_name )
print('💤 Waiting for report messages. To exit, press CTRL+ C')

channel.start_consuming()