import json
from typing import Dict

import beanstalkc

from component_reuse.abcs.queue_adapter_abc import QueueAdapterABC
from component_reuse.logger import LOG


class BeanstalkQueueAdapter(QueueAdapterABC):
    """A class representing a Beanstalk Queue Adapter."""

    def __init__(self, host: str, port: int, queue: str) -> None:
        """Initialize a BeanstalkQueueAdapter instance."""
        self.host = host
        self.port = port
        self.queue = queue
        self.connection = None

    def connect(self) -> None:
        """Establish a connection to the Beanstalk server."""
        try:
            self.connection = beanstalkc.Connection(host=self.host, port=self.port)
            LOG.info(f"Connected to Beanstalkd at {self.host}:{self.port}")
        except beanstalkc.SocketError as e:
            LOG.error(f"Error connecting to Beanstalkd: {e}")
            raise e

    def dispatch(self, payload: Dict) -> None:
        """Dispatch a payload to the Beanstalk queue."""
        if not self.connection:
            self.connect()

        try:
            LOG.debug(f"Using queue: {self.queue}")
            LOG.debug(f"Dispatching payload: {json.dumps(payload)}")
            self.connection.use(self.queue)
            self.connection.put(json.dumps(payload))
            LOG.debug(f"Dispatched payload to {self.queue}")
        except Exception as e:
            LOG.error(f"Error dispatching payload to {self.queue} queue: {e}")
            raise e

    def consume(self) -> None:
        """Consume method implementation to avoid abstract class errors."""
        LOG.info("Consume method not implemented for this adapter.")
        raise NotImplementedError("Consume method is not implemented.")

    def disconnect(self) -> None:
        """Close the connection to the Beanstalk server."""
        try:
            if self.connection:
                self.connection.close()
                LOG.info("Disconnected from Beanstalkd")
        except Exception as e:
            LOG.error(f"Error disconnecting from Beanstalkd: {e}")
