"""Token manager module."""

import uuid
import json

import pika


class TokenManager:
    """Token manager class."""

    def __init__(self) -> None:
        """Initialize the token manager."""
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
        self.response = None
        self.correlation_id = None

    def on_response(self, ch, method, properties, body) -> None:
        """Handle the response."""
        if self.correlation_id == properties.correlation_id:
            self.response = json.loads(body)

    def validate(self, token: str) -> bool:
        """Check if the token is valid."""
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key="auth_queue",
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
            ),
            body=json.dumps({"token": token}),
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response.get("valid", False)
