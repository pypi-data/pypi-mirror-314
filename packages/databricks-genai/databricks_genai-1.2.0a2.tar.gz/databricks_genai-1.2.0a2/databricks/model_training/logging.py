"""Logging utilities"""
import logging
from contextlib import contextmanager

from rich.console import Console

from databricks.model_training.api.utils import is_running_in_databricks_notebook


def get_console() -> Console:
    if is_running_in_databricks_notebook():
        return Console(force_jupyter=True)
    return Console()


console = get_console()


@contextmanager
def temp_log_level(name: str, level: int):
    logger = logging.getLogger(name)
    # Save old level
    old_level = logger.getEffectiveLevel()
    # Set new level
    logger.setLevel(level)
    try:
        yield
    finally:
        # Restore old level
        logger.setLevel(old_level)
