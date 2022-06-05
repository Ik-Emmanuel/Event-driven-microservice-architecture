import pika, json
from app import Product, db

params = pika.URLParameters('amqps://svhpokuu:4Wg0rwXBfFpOlYL-jPpINpZ-j7erT5KH@woodpecker.rmq.cloudamqp.com/svhpokuu')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print("getting new")
    print('Received new in main')
    data = json.loads(body)
    print(properties.content_type)


    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print("Product created")

    elif properties.content_type== 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print("Product updated")

    elif properties.content_type== 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print("Product deleted")


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
print('Started Consuming')

channel.start_consuming()
channel.close()