"""RabbitMQ consumer for the auth service."""

import json
import logging

import pika
from auth_service.utils.token_manager import validate_token

logger = logging.getLogger(__name__)


def on_request(ch, method, properties, body):
    """Callback function for the RabbitMQ consumer.

    Args:
        ch (pika.channel.Channel): The channel object.
        method (pika.spec.Basic.Deliver): The method object.
        properties (pika.spec.BasicProperties): The properties object.
        body (str): The message body.
    """
    logger.info(" [x] Received %s", body)
    token = json.loads(body)
    response = validate_token(token)
    ch.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=json.dumps({"valid": response}),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    """Starts the RabbitMQ consumer."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )
    channel = connection.channel()

    channel.queue_declare(queue="auth_queue", durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="auth_queue", on_message_callback=on_request)

    logger.info(" [x] Awaiting RPC requests")
    channel.start_consuming()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    start_consumer()
