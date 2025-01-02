"""Token manager module."""

import json
import time
import uuid

import pika


class TokenManager:
    """Token manager class."""

    def __init__(self) -> None:
        """Initialize the token manager."""
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None
        self.correlation_id = None
        self.connect()

    def connect(self):
        """Establish connection to RabbitMQ server with retry logic."""
        while True:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters("localhost")
                )
                self.channel = self.connection.channel()
                self.callback_queue = self.channel.queue_declare(
                    queue="", exclusive=True
                ).method.queue
                self.channel.basic_consume(
                    queue=self.callback_queue,
                    on_message_callback=self.on_response,
                    auto_ack=True,
                )
                break
            except pika.exceptions.AMQPConnectionError:
                print("Connection failed, retrying in 5 seconds...")
                time.sleep(5)

    def on_response(self, ch, method, properties, body) -> None:
        """Handle the response."""
        if self.correlation_id == properties.correlation_id:
            self.response = json.loads(body)

    def validate(self, token: str) -> bool:
        """Check if the token is valid."""
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key="auth_queue",
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.correlation_id,
                ),
                body=json.dumps({"token": token}),
            )
        except pika.exceptions.AMQPConnectionError:
            print("Connection lost, reconnecting...")
            self.connect()
            return self.validate(token)

        while self.response is None:
            try:
                self.connection.process_data_events()
            except pika.exceptions.AMQPConnectionError:
                print("Connection lost during processing, reconnecting...")
                self.connect()
                return self.validate(token)

        return self.response.get("valid", False)
