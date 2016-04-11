import logging

import pika
from pika import adapters


logger = logging.getLogger('tornado_app.queue_client')


class QueueClient():
    def __init__(self, queue, callback):
        self.queue = queue
        self.message_handler = callback
        parameters = pika.ConnectionParameters('localhost')
        self.connection = adapters.TornadoConnection(parameters,
                                                     self.on_connected)

    def on_connected(self, connection):
        logger.debug("Connected to queue")
        connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        logger.debug("Channel open")
        self.channel = channel
        channel.queue_declare(queue=self.queue, durable=True,
                              exclusive=False, auto_delete=False,
                              callback=self.on_queue_declared)

    def on_queue_declared(self, frame):
        self.consumer_tag = self.channel.basic_consume(self.on_message,
                                                       self.queue)

    def on_message(self, channel, basic_deliver, properties, body):
        self.message_handler(body)
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        self.channel.basic_ack(delivery_tag)

    def stop(self):
        self.channel.basic_cancel(self.on_cancel_ok, self.consumer_tag)

    def on_cancel_ok(self):
        self.channel.close()

