import pika


class RabbitmqConsumer:
    def __init__(self, host='localhost', port=5672, user='guest', password='guest', virtual_host='/', exchange='',
                 routing_key=''):
        self.params = pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host,
                                                credentials=pika.PlainCredentials(username=user, password=password))
        self.exchange = exchange
        self.routing_key = routing_key
        self.channel = None
        self.declare_channel()

    def declare_channel(self):
        connection = pika.BlockingConnection(self.params)
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')
        self.channel.queue_declare(queue=self.routing_key, durable=True)
        self.channel.queue_bind(exchange=self.exchange, routing_key=self.routing_key, queue=self.routing_key)

    def consume(self, callback):
        self.channel.basic_consume(queue=self.routing_key, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
