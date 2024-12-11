import logging
import sys
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter
from typing_extensions import Self

from cnrgh_dl import config


class Logger:
    """Application logger."""

    __instance = None
    """Logger instance."""

    def __init__(self: Self) -> None:
        """Initialize a logger. This constructor should not be called directly.
        To obtain a logger instance, call ``Logger.getinstance()``.

        :raises RuntimeError: The Logger constructor was called directly, instead of calling ``Logger.getinstance()``.
        """
        if Logger.__instance is not None:
            msg = (
                "This class can not be instantiated. "
                "Please use the get_instance method instead."
            )
            raise RuntimeError(
                msg,
            )

    @staticmethod
    def _setup_rotating_file_handler() -> RotatingFileHandler:
        """Set up a handler for logging to a set of files, which switches from one file
        to the next when the current file reaches a certain size. The level of this handler is fixed to `DEBUG`.

        :return: The configured rotating file handler.
        """
        # Rotate before exceeding 1 Mb.
        rf_handler = RotatingFileHandler(
            config.LOG_SAVE_FILE, maxBytes=1_000_000, backupCount=3
        )
        rf_formatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s %(message)s"
        )
        rf_handler.setFormatter(rf_formatter)
        rf_handler.setLevel(logging.DEBUG)
        return rf_handler

    @staticmethod
    def _setup_console_handler() -> logging.StreamHandler:  # type: ignore[type-arg]
        """Set up a handler for writing colored logs to the console.
        The level of this handler is controlled by the `CNRGHDL_LOG_LEVEL` environment variable.

        :return: The configured stream handler.
        """
        console_formatter = ColoredFormatter(
            "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red",
            },
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(config.LOG_LEVEL)
        return console_handler

    @staticmethod
    def get_instance() -> logging.Logger:
        """Get the logger instance.

        :return: The logger instance.
        """
        if Logger.__instance is None:
            # Get the root logger.
            logger = logging.getLogger(__package__)
            # Explicitly set the logger level to DEBUG,
            # as otherwise it would have inherited from the default WARNING level of the root logger.
            logger.setLevel(logging.DEBUG)
            # Add the console and file handlers.
            logger.addHandler(Logger._setup_console_handler())
            logger.addHandler(Logger._setup_rotating_file_handler())

            Logger.__instance = logger

        return Logger.__instance
