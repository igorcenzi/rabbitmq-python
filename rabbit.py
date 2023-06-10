import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='ex.hash2', exchange_type='x-consistent-hash', durable=True)
for q in [{'queue': 'q.nova1', 'key': '1'}, {'queue': 'q.nova2', 'key': '2'}]:
    channel.queue_declare(queue=q['queue'], durable=True)
    channel.queue_bind(exchange='ex.hash2', queue=q['queue'], routing_key=q['key'])
    channel.queue_purge(queue=q['queue'])

n = 100000

for rk in list(map(lambda s: str(s), range(0, n))):
    message = f'Hello World! {rk}'
    channel.basic_publish(exchange='ex.hash2',
                        routing_key=rk,
                        body=message
                        )

print('[x] Sent "Hello World!"')

connection.close()