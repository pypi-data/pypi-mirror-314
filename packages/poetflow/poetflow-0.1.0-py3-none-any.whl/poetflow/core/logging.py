"""Logging configuration for PoetFlow."""

import logging


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration.

    Args:
        log_level: Logging level
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Create logger
    logger = logging.getLogger("poetflow")
    logger.setLevel(getattr(logging, log_level.upper()))
