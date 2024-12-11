from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import FrameType


import signal
import sys
import threading

from typing_extensions import Self

from cnrgh_dl.logger import Logger

logger = Logger.get_instance()
"""Module logger instance."""


class CustomSigIntHandler:
    """Define and register a custom SIGINT handler,
    asking the user for confirmation before exiting.
    """

    def __init__(self: Self) -> None:
        """Create a CustomSigIntHandler instance."""
        self._lock = threading.Lock()

    def register_custom_handler(self: Self) -> None:
        """Register the custom SIGINT handler."""
        signal.signal(signal.SIGINT, self._custom_sigint_handler)

    def _custom_sigint_handler(
        self: Self,
        signum: int,  # noqa: ARG002
        frame: FrameType | None,  # noqa: ARG002
    ) -> None:
        """Custom SIGINT signal handler that asks for user confirmation before exiting."""
        with self._lock:
            # Temporarily ignore subsequent SIGINT signals while handling the current one.
            signal.signal(signal.SIGINT, signal.SIG_IGN)

            try:
                while True:
                    response = (
                        input(
                            "You are about to stop the execution of cnrgh-dl. Are you sure ? (y/n) : "
                        )
                        .strip()
                        .lower()
                    )
                    if response in {"y", "n"}:
                        break
                    print("Please enter 'y' or 'n'.")  # noqa: T201
                if response == "y":
                    logger.info("Exiting cnrgh-dl...")
                    sys.exit(0)
                else:
                    logger.info("Resuming execution of cnrgh-dl...")
            except EOFError:
                logger.info("Received EOF. Resuming execution of cnrgh-dl...")
            finally:
                # Register the custom signal handler again.
                signal.signal(signal.SIGINT, self._custom_sigint_handler)
