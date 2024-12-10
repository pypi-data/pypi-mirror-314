import json

from component_reuse.adapters.abstract_beanstalk_adapter import BeanstalkQueueAdapter
from component_reuse.adapters.abstract_rabbitmq_adapter import RabbitMQAdapter
from component_reuse.logger import LOG
from component_reuse.settings.benstalk_adapter_settings import (
    beanstalk_adapter_settings,
)
from component_reuse.settings.rabbitmq_adapter_settings import rabbitmq_adapter_settings

# Initialize BeanstalkQueueAdapter
beanstalk_adapter = BeanstalkQueueAdapter(
    host=beanstalk_adapter_settings.BEANSTALK_HOST,
    port=beanstalk_adapter_settings.BEANSTALK_PORT,
    queue=beanstalk_adapter_settings.BEANSTALK_QUEUE_NAME,
)

# Connect to Beanstalk
try:
    if beanstalk_adapter.connect():
        LOG.info("Connection to Beanstalk established successfully.")
except Exception as e:
    LOG.error(f"Failed to connect to Beanstalk: {e}")
    raise e


def on_message_callback(body):
    try:
        # Decode and process the RabbitMQ message
        message = body.decode("utf-8")
        LOG.info(f"Received raw message from RabbitMQ: {message}")

        # Try to parse the message as JSON
        try:
            json_message = json.loads(message)
            LOG.info(
                f"Received message from RabbitMQ as JSON: {json.dumps(json_message, indent=2)}"
            )
        except json.JSONDecodeError:
            LOG.warning(f"Received non-JSON message: {message}")
            json_message = {"message": message}  # Wrap non-JSON messages as plain text

        # Dispatch message to Beanstalk
        LOG.debug("Attempting to dispatch message to Beanstalk")
        beanstalk_adapter.dispatch(json_message)
        LOG.info(
            f"Message dispatched to Beanstalk queue {beanstalk_adapter_settings.BEANSTALK_QUEUE_NAME} successfully."
        )

    except Exception as e:
        LOG.error(f"Unexpected error in message processing: {e}")


# Initialize the RabbitMQAdapter
rabbitmq_adapter = RabbitMQAdapter(
    host=rabbitmq_adapter_settings.RABBITMQ_HOST,
    port=int(rabbitmq_adapter_settings.RABBITMQ_PORT),
    username=rabbitmq_adapter_settings.RABBITMQ_USERNAME,
    password=rabbitmq_adapter_settings.RABBITMQ_PASSWORD.get_secret_value(),
    ssl_options=None,
    queue_name=rabbitmq_adapter_settings.RABBITMQ_CONSUME_QUEUE_NAME,
    has_error_queue=True,
    error_queue_name=rabbitmq_adapter_settings.RABBITMQ_ERROR_QUEUE_NAME,
    max_retries=rabbitmq_adapter_settings.RABBITMQ_MAX_RETRIES,
    on_message_callback=on_message_callback,
    consumption_limit=rabbitmq_adapter_settings.RABBITMQ_MESSAGE_CONSUMPTION_LIMIT,
    message_auto_ack=rabbitmq_adapter_settings.RABBITMQ_MESSAGE_AUTO_ACK,
    message_prefetch_count=rabbitmq_adapter_settings.RABBITMQ_MESSAGE_PREFETCH_COUNT,
)

# Test the connection to RabbitMQ and consume messages
try:
    if rabbitmq_adapter.connect():
        LOG.info("Connection to RabbitMQ established successfully.")
        rabbitmq_adapter.consume()
    else:
        LOG.error("Failed to connect to RabbitMQ.")
except Exception as e:
    LOG.error(f"Connection to RabbitMQ failed: {e}")
