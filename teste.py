import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)
n = 1000000
for x in range(n):
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body='H')
print(" [x] Sent 'Hello World!'")
connection.close()