from time import sleep
from typing import Any
from typing import Union

import pika

from component_reuse.abcs.queue_adapter_abc import QueueAdapterABC
from component_reuse.logger import LOG


class RabbitMQAdapter(QueueAdapterABC):
    """A class to manage RabbitMQ queue operations with enhanced error
    handling."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        ssl_options: Union[pika.SSLOptions, None],
        queue_name: str,
        has_error_queue: bool = False,
        error_queue_name: str = None,
        has_dead_letter_queue: bool = False,
        dead_letter_queue_name: str = None,
        max_retries: int = 3,
        on_message_callback: Any = None,
        consumption_limit: int = -1,
        message_auto_ack: bool = False,
        message_prefetch_count: int = 0,
    ) -> None:
        """Initialize the RabbitMQAdapter with RabbitMQ connection
        parameters."""
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssl_options = ssl_options
        self.connection = None
        self.channel = None
        self.on_message_callback = on_message_callback
        self.queue_name = queue_name
        self.has_error_queue = has_error_queue
        self.error_queue_name = error_queue_name
        self.has_dead_letter_queue = has_dead_letter_queue
        self.dead_letter_queue_name = dead_letter_queue_name
        self.max_retries = max_retries
        self.consumption_limit = consumption_limit
        self.consumed_messages = 0
        self.message_auto_ack = message_auto_ack
        self.message_prefetch_count = message_prefetch_count

    def connect(self) -> bool:
        """Establish a connection to the RabbitMQ server."""
        retries = 0
        while retries < self.max_retries:
            try:
                credentials = pika.PlainCredentials(self.username, self.password)
                parameters = pika.ConnectionParameters(
                    host=self.host, port=self.port, credentials=credentials
                )
                parameters.ssl_options = self.ssl_options

                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()

                self.channel.queue_declare(queue=self.queue_name, durable=True)
                if self.has_error_queue:
                    self.channel.queue_declare(
                        queue=self.error_queue_name, durable=True
                    )
                if self.has_dead_letter_queue:
                    self.channel.queue_declare(
                        queue=self.dead_letter_queue_name, durable=True
                    )

                self.channel.basic_qos(prefetch_count=self.message_prefetch_count)
                LOG.info(f"Connected to RabbitMQ server on {self.host}:{self.port}")
                return True
            except pika.exceptions.AMQPError as e:
                retries += 1
                LOG.error(f"Connection attempt {retries} failed: {e}")
                sleep(1)
                self.disconnect()
            except Exception as e:
                LOG.error(f"Unexpected error during connection: {e}")
                self.disconnect()
                raise pika.exceptions.AMQPError(
                    "Failed to connect after multiple retries."
                )
        raise pika.exceptions.AMQPError("Failed to connect after multiple retries.")

    def consume(self) -> None:
        """Begin consuming messages from the RabbitMQ queue."""
        try:
            LOG.info("Starting message consumption...")
            if self.consumption_limit == -1:
                self.channel.basic_consume(
                    queue=self.queue_name,
                    auto_ack=self.message_auto_ack,
                    on_message_callback=self.run,
                )
                self.channel.start_consuming()
            elif self.consumption_limit > 0:
                self._consume_with_limits()
            else:
                LOG.error(f"Invalid consumption limit: {self.consumption_limit}.")
        except Exception as e:
            LOG.error(f"Error consuming the message: {e}")
            self.disconnect()
            raise e

    def _consume_with_limits(self) -> None:
        """Consume messages with a limit on the number of messages."""
        try:
            while self.consumed_messages < self.consumption_limit:
                method_frame, properties, body = self.channel.basic_get(
                    queue=self.queue_name, auto_ack=self.message_auto_ack
                )
                if method_frame:
                    self.run(self.channel, method_frame, properties, body)
                    self.consumed_messages += 1
                else:
                    LOG.info("Heartbeat - No messages in queue.")
                    sleep(5)
            LOG.info(
                f"Consumed the maximum number of messages: {self.consumption_limit}"
            )
        except Exception as e:
            LOG.error(f"Error during limited consumption: {e}")
            raise e

    def run(self, channel: Any, method: Any, properties: Any, body: bytes) -> None:
        """Process the incoming message and manage retries."""
        try:
            self.on_message_callback(body)
            if not self.message_auto_ack:
                channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            LOG.error(f"Error processing message: {e}")
            requeue_count = (
                properties.headers.get("requeue_count", 0) if properties.headers else 0
            )
            if requeue_count < self.max_retries:
                self._requeue_message(channel, body, requeue_count)
            else:
                self._move_to_error_queue(channel, body)

    def _requeue_message(self, channel: Any, body: bytes, requeue_count: int):
        """Helper function to requeue a message."""
        headers = {"requeue_count": requeue_count + 1}
        channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,
                headers=headers,
            ),
        )
        LOG.info(
            f"Message requeued to {self.queue_name} with requeue count {requeue_count + 1}."
        )

    def _move_to_error_queue(self, channel: Any, body: bytes):
        """Helper function to move a message to the error queue."""
        if self.has_error_queue:
            channel.basic_publish(
                exchange="",
                routing_key=self.error_queue_name,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    headers={"requeue_count": 0},
                ),
            )
            LOG.info(f"Message moved to error queue {self.error_queue_name}.")
        else:
            LOG.warning("Error queue is not configured. Message will not be requeued.")

    def dispatch(self, body: Any) -> None:
        """Dispatches the given data to the RabbitMQ queue."""
        retries = 0
        while retries < 3:
            try:
                if not self.connection or self.connection.is_closed:
                    LOG.debug(f"Reconnecting to {self.queue_name}")
                    self.connect()
                self.channel.basic_publish(
                    exchange="",
                    routing_key=self.queue_name,
                    body=body,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    ),
                )
                break
            except Exception as e:
                sleep(0.5)
                self.connect()
                LOG.error(
                    f"Error dispatching data to the {self.queue_name} queue, retrying... : {e}"
                )
                retries += 1
                if retries >= 3:
                    LOG.error(
                        f"Maximum retries for dispatch to the {self.queue_name} reached: {e}"
                    )
                    raise e

    def disconnect(self) -> bool:
        """Close the connection to the RabbitMQ server."""
        try:
            if self.channel:
                self.channel.stop_consuming()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                LOG.info(f"Disconnected from RabbitMQ on {self.host}:{self.port}")
            return True
        except Exception as e:
            LOG.error(f"Error during disconnection: {e}")
            raise pika.exceptions.AMQPError(f"Error during disconnection: {e}")
