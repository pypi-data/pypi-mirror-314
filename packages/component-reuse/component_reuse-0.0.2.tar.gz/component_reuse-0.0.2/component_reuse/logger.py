import logging

LOG = logging.getLogger(__name__)

LOG.warning(
    "This package is proprietary. Unauthorized use or distribution is prohibited."
)


class CustomLogger:
    """Extends the native logging module."""

    @staticmethod
    def logger() -> logging.Logger:
        """Handles logs."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger


LOG = CustomLogger.logger()
